# utils.py
from django.conf import settings
from django.db import connections, OperationalError
from .models import Pincode, Address
import re

def connectDatabase(alias='default'):
    """
    Try to ensure DB connection. Return True or raise OperationalError.
    """
    try:
        conn = connections[alias]
        conn.ensure_connection()
        return True
    except OperationalError as e:
        raise

def getAddressValidationRules():
    """
    Return a list/dict of validation rules.
    """
    rules = {
        "house_no": {"required": True, "max_length": 64, "pattern": r"^[A-Za-z0-9\/\-\s]+$"},
        "street": {"required": True, "max_length": 128},
        "landmark": {"required": False, "max_length": 128},
        "area": {"required": True, "max_length": 128},
        "pincode": {"required": True, "pattern": r"^\d{5,6}$"},
    }
    return rules

def getAddressErrors():
    """
    Return standard error codes/messages used by API.
    """
    return {
        "E001": "House/Flat number invalid or contains special characters",
        "E002": "Street is required or too long",
        "E003": "Area is required or too long",
        "E004": "Pincode invalid",
        "E005": "Pincode details not found",
        "E006": "Database connection error",
    }

def getLocationDetails(pinCode):
    """
    Try to fetch country, state, district from Pincode model.
    Returns (country, state, district) or raise ValueError if not found.
    """
    try:
        p = Pincode.objects.filter(pincode=pinCode).first()
        if p:
            return {"country": p.country, "state": p.state, "district": p.district}
        else:
            raise ValueError("Pincode not found")
    except Exception as e:
        raise

def addressFieldValidation(houseNo, street, landmark, area, pinCode):
    """
    Validate fields and return (True, None) on success or (False, error_dict)
    error_dict: {"field": "houseNo", "code": "E001", "message": "..."}
    """
    rules = getAddressValidationRules()
    errors = getAddressErrors()

    # houseNo
    if rules["house_no"]["required"] and (houseNo is None or houseNo.strip() == ""):
        return False, {"field": "houseNo", "code": "E001", "message": errors["E001"]}
    if len(houseNo) > rules["house_no"]["max_length"]:
        return False, {"field": "houseNo", "code": "E001", "message": "House number too long"}
    if not re.match(rules["house_no"]["pattern"], houseNo):
        return False, {"field": "houseNo", "code": "E001", "message": errors["E001"]}

    # street
    if rules["street"]["required"] and (street is None or street.strip() == ""):
        return False, {"field": "street", "code": "E002", "message": errors["E002"]}
    if len(street) > rules["street"]["max_length"]:
        return False, {"field": "street", "code": "E002", "message": errors["E002"]}

    # area
    if rules["area"]["required"] and (area is None or area.strip() == ""):
        return False, {"field": "area", "code": "E003", "message": errors["E003"]}
    if len(area) > rules["area"]["max_length"]:
        return False, {"field": "area", "code": "E003", "message": errors["E003"]}

    # pincode
    if rules["pincode"]["required"] and (pinCode is None or pinCode.strip() == ""):
        return False, {"field": "pincode", "code": "E004", "message": errors["E004"]}
    if not re.match(rules["pincode"]["pattern"], pinCode):
        return False, {"field": "pincode", "code": "E004", "message": errors["E004"]}

    # Attempt to fetch the location details
    try:
        loc = getLocationDetails(pinCode)
    except ValueError:
        return False, {"field": "pincode", "code": "E005", "message": errors["E005"]}
    except Exception:
        return False, {"field": "pincode", "code": "E006", "message": "Database error"}

    # If we reach here, all checks passed
    return True, None

def insertAddress(user_id, flat_no, street, landmark, area, pincode, district, state, country):
    """
    Insert address into DB and return Address instance.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)
    addr = Address.objects.create(
        user=user,
        flat_no=flat_no,
        street=street,
        landmark=landmark or "",
        area=area,
        pincode=pincode,
        district=district,
        state=state,
        country=country,
    )
    return addr

