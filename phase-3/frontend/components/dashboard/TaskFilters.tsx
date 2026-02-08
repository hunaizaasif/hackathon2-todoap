"use client";

interface TaskFiltersProps {
  filter: "all" | "pending" | "in_progress" | "complete";
  onFilterChange: (filter: "all" | "pending" | "in_progress" | "complete") => void;
}

export function TaskFilters({ filter, onFilterChange }: TaskFiltersProps) {
  return (
    <div className="flex gap-2">
      <button
        onClick={() => onFilterChange("all")}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          filter === "all"
            ? "bg-primary text-primary-foreground"
            : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
        }`}
      >
        All
      </button>
      <button
        onClick={() => onFilterChange("pending")}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          filter === "pending"
            ? "bg-primary text-primary-foreground"
            : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
        }`}
      >
        Pending
      </button>
      <button
        onClick={() => onFilterChange("in_progress")}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          filter === "in_progress"
            ? "bg-primary text-primary-foreground"
            : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
        }`}
      >
        In Progress
      </button>
      <button
        onClick={() => onFilterChange("complete")}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          filter === "complete"
            ? "bg-primary text-primary-foreground"
            : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
        }`}
      >
        Complete
      </button>
    </div>
  );
}
