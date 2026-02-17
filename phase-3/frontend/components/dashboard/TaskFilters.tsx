"use client";

interface TaskFiltersProps {
  filter: "all" | "pending" | "in_progress" | "complete";
  onFilterChange: (filter: "all" | "pending" | "in_progress" | "complete") => void;
}

export function TaskFilters({ filter, onFilterChange }: TaskFiltersProps) {
  const filters = [
    { value: "all", label: "🌟 All", gradient: "from-purple-600 to-pink-600" },
    { value: "pending", label: "⏳ Pending", gradient: "from-yellow-500 to-orange-500" },
    { value: "in_progress", label: "⚡ In Progress", gradient: "from-blue-500 to-cyan-500" },
    { value: "complete", label: "✓ Complete", gradient: "from-green-500 to-emerald-500" },
  ];

  return (
    <div className="flex gap-2 flex-wrap">
      {filters.map((f) => (
        <button
          key={f.value}
          onClick={() => onFilterChange(f.value as any)}
          className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 transform hover:scale-105 ${
            filter === f.value
              ? `bg-gradient-to-r ${f.gradient} text-white shadow-lg`
              : "glass-effect text-gray-700 dark:text-gray-200 hover:shadow-md"
          }`}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
}
