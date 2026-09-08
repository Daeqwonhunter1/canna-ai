import SearchBar from "@/components/SearchBar";

export default function Home() {
  return (
    <main className="mx-auto max-w-[640px] px-5 py-12">
      <h1 className="font-display text-[2rem] font-semibold tracking-tight mb-1">Canna-AI</h1>
      <p className="text-muted mb-8 text-[0.95rem]">
        Search a strain or brand. Same strain, different brands — see them side by side before you pick.
      </p>
      <SearchBar />
    </main>
  );
}