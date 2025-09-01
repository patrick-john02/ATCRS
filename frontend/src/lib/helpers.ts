//pso formatter
export function formatToPeso(amount: number): string {
    return new Intl.NumberFormat("en-PH", {
        style: "currency",
        currency: "PHP",
        minimumFractionDigits: 2,
    }).format(amount);
}

//meters formatter
export function parseMeters(value: string | number | null, decimals = 2): string {
  if (value === null || value === undefined) return "—";

  const num = typeof value === "string" ? parseFloat(value) : value;

  if (isNaN(num)) return "—";

  return num.toFixed(decimals);
}


//date formatter
export function formatDateTime(dateString: string): string {
  if (!dateString) return "—";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return "Invalid Date";

  return date.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

//project helper
export function getProjectTypeBadge(projectName: string) {
  const name = projectName.toLowerCase();
  if (name.includes("building") || name.includes("tower") || name.includes("structure")) {
    return { label: "Vertical", class: "bg-purple-100 text-purple-800" };
  } else if (name.includes("road") || name.includes("bridge") || name.includes("highway")) {
    return { label: "Horizontal", class: "bg-blue-100 text-blue-800" };
  }
  return { label: "General", class: "bg-gray-100 text-gray-800" };
}