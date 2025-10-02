import { useEffect, useState } from "react"

export default function LeBouton()
{
  const [value, setValue] = useState(0);

  const fetchApi = async () => {
    const req = await fetch("/api/access", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
    const data = await req.json();
    console.log(data);
    if (req.ok) {
      setValue(parseInt(data.counter));
    }
  }
  useEffect(() => {
    fetchApi();
  }, []);
  return (
    <button onClick={fetchApi}>JE SUIS LE BOUTON QUI SENT BON {value}</button>
  )
}