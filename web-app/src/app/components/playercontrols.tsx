"use client";

import React, { useState } from "react";
import { PlayerType } from "../types";
import { SegmentBoundaryTriggerNode } from "next/dist/next-devtools/userspace/app/segment-explorer-node";

async function updateName(id: number, newName: string) {
  const res = await fetch(`/api/player/${id}/name`, {
    method: "PUT",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({name: newName})
  });
  const data = await res.json();
  if (!res.ok)
    throw new Error(data.error || "Failed to update name");
  return data.player;
}

export default function PlayerControls({player, onPlayerUpdate}: {player: PlayerType, onPlayerUpdate: (updatedPlayer: PlayerType) => void}) {
  const [nameField, setNameField] = useState(player.name);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const updated = await updateName(player.id, nameField);
      console.log(updated);
      onPlayerUpdate(updated);
    } catch (err) {
      alert((err as Error).message);
      setNameField(player.name);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={nameField} type="text" disabled={loading} onChange={(e)=>setNameField(e.target.value)}></input>
      <input type="submit" disabled={loading} value={loading ? "Sending..." : "Send"}></input>
    </form>
  );
}
