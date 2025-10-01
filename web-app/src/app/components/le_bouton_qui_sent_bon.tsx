import { useEffect, useState } from "react"

export default function LeBouton()
{
  const [value, setValue] = useState(0);

  useEffect(() => {
    const req = await fetch("/api/access", {
      method: "GET",
      headers: { "Content-Type": "application/json"},
    })
    const data = await req.json();
    if (req.ok) {
      setValue(parseInt(data.counter));
    }
  }, []);
  return (
    <button value={value}></button>
  )
}