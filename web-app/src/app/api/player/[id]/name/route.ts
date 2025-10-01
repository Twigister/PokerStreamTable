// app/api/player/[id]/name/route.ts
import { NextRequest, NextResponse } from "next/server"

// Fake in-memory DB
let playersDB: Record<number, { name: string }> = {
  1: { name: "Armand" },
  2: { name: "Max" },
}

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const { id } = await params
  const playerId = parseInt(id)

  if (!playersDB[playerId]) {
    return NextResponse.json({ error: "Player not found" }, { status: 404 })
  }

  const data = await req.json() // expects { name: "newName" }
  if (!data.name || typeof data.name !== "string") {
    return NextResponse.json({ error: "Invalid name" }, { status: 400 })
  }

  playersDB[playerId].name = data.name;

  return NextResponse.json({ success: true, player: { id: playerId, name: playersDB[playerId].name }})
}
