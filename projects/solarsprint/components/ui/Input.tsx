'use client';

export type InputProps = {
  id: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  autoComplete?: string;
  className?: string;
};

export function Input({
  id,
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  required = false,
  disabled = false,
  autoComplete,
  className = '',
}: InputProps) {
  const baseInputStyles = 'w-full px-4 py-3 border rounded-lg transition-colors focus:outline-none';
  const normalStyles = 'border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent';
  const errorStyles = 'border-red-500 focus:ring-2 focus:ring-red-500';
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed bg-gray-50' : '';

  return (
    <div className={`w-full ${className}`}>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <input
        id={id}
        name={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        autoComplete={autoComplete}
        className={`${baseInputStyles} ${error ? errorStyles : normalStyles} ${disabledStyles}`}
      />
      
      {error && (
        <p className="text-red-600 text-sm mt-1">{error}</p>
      )}
    </div>
  );
}

export default Input;

