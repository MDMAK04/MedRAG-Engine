export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">

      <div>
        <h1 className="text-sm font-semibold">
          Medical Research Assistant
        </h1>

        <p className="mt-0.5 text-xs text-gray-500">
          Search and analyze scientific literature
        </p>
      </div>

      <div className="flex items-center gap-2 rounded-full border border-gray-200 px-3 py-1.5">

        <span className="h-2 w-2 rounded-full bg-green-500" />

        <span className="text-xs font-medium text-gray-600">
          System ready
        </span>

      </div>

    </header>
  )
}