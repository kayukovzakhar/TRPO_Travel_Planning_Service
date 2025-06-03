// components/ui/card.tsx
import React from 'react'

export const Card = ({ children, className = "" }: { children: React.ReactNode, className?: string }) => (
  <div className={`p-4 bg-white shadow-md rounded-2xl border ${className}`}>
    {children}
  </div>
)

export const CardContent = ({ children, className = "" }: { children: React.ReactNode, className?: string }) => (
  <div className={`p-4 ${className}`}>
    {children}
  </div>
)
