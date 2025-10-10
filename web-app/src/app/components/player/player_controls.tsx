"use client";

import React, { useState } from "react";
import { PlayerType } from "../types";
import styles from "./player_controls.module.css"

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
    <div className={styles.controls}>
      <div className={styles.pannel}>
        <div className={styles.controlButtons}>
          <form onSubmit={handleSubmit}>
            <input value={nameField} type="text" disabled={loading} onChange={(e) => setNameField(e.target.value)}></input>
          </form>
        </div>
        <div>
          <form>
            <input type="button" value="Check/Call" className={styles.controlButton}/>
            <input type="button" value="Raise" className={styles.controlButton}/>
            <input type="button" value="Fold" className={styles.controlButton}/>
          </form>
        </div>
      </div>
      <div className={styles.sideButtons}>
        <span className={styles.sideButton}>A</span>
        <span className={styles.sideButton}>B</span>
        <span className={styles.sideButton}>C</span>
      </div>
    </div>
  );
}
