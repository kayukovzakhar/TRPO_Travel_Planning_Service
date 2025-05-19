// components/ui/button.tsx
import React from 'react'

export const Button = ({ children, className }: { children: React.ReactNode, className: string }) => (
  <button className={`px-6 py-2 rounded-2xl text-lg shadow-md ${className}`}>
    {children}
  </button>
)
