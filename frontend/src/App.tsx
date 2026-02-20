import { Button } from "@/components/ui/button"
import { useState } from "react"

export default function App() {
  const [teste, useTeste] = useState(0)

  const sum = () => {
    useTeste(teste + 1)
  }

  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <Button onClick={sum}>Click me</Button>
      <p>{teste != 0 ? teste : ""}</p>
    </div>
  )
}

