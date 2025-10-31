// InputField component
import React from 'react'

/**
 * Simple controlled input with label animation.
 * Props: label, type, name, value, onChange, placeholder
 */
export default function InputField({ label, type = 'text', name, value, onChange, placeholder }) {
  return (
    <div className="input-group">
      <input
        className="input-field"
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder || ''}
        autoComplete="off"
      />
      <label htmlFor={name} className={value ? 'filled' : ''}>{label}</label>
    </div>
  )
}
