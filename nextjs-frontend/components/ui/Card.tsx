import { ReactNode } from "react";

interface CardProps {
  title?: string;
  description?: string;
  children?: ReactNode;
  className?: string;
}

export default function Card({
  title,
  description,
  children,
  className = "",
}: CardProps) {
  return (
    <div
      className={`rounded-lg border bg-white p-6 shadow-sm dark:bg-gray-800 dark:border-gray-700 ${className}`}
    >
      {title && (
        <h3 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>
      )}
      {description && (
        <p className="mb-4 text-gray-600 dark:text-gray-400">{description}</p>
      )}
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
}
