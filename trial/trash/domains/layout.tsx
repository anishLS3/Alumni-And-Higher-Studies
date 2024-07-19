import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Domains",
    description: "Create Domains",
  };

export default function ProfileLayout({children} : {children: React.ReactNode}){
    return (
        <main className="h-full">
            {children}
        </main>
    )
}