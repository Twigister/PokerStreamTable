"use client";

import React, { useState } from "react";
import { PlayerType } from "../types";
import styles from "./player_controls.module.css"

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function PlayerControls({player, onUnseat}: {player: PlayerType, onUnseat: (playerId: number) => void}) {
  const [loading, setLoading] = useState(false);

  async function handleUnseat() {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/users/unseat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: player.id }),
      });
      if (!response.ok) {
        throw new Error("Failed to unseat player.");
      }
      onUnseat(player.id);
    } catch (err) {
      alert((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.controls}>
      <div className={styles.pannel}>
        <div>
          <form>
            <input type="button" value="Check/Call" className={styles.controlButton}/>
            <input type="button" value="Raise" className={styles.controlButton}/>
            <input type="button" value="Fold" className={styles.controlButton}/>
            <input type="button" value="Unseat" className={styles.controlButton} disabled={loading} onClick={handleUnseat}/>
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
