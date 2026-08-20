"use client";

import React, { useState } from "react";
import { PlayerType } from "../../types";
import styles from "./player_controls.module.css"

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function PlayerControls({player, onUnseat}: {player: PlayerType, onUnseat: (playerId: number) => void}) {
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"game" | "money" | "other">("game");

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

  function selectTab(tab: "game" | "money" | "other") {
    setActiveTab(tab);
  }

  return (
    <section className={styles.controls} aria-label={`Controls for ${player.name}`}>
      <div
        className={styles.panel}
        id={`player-controls-${player.id}`}
        role="tabpanel"
        aria-label={`${activeTab} actions`}
      >
        {activeTab === "game" && (
          <div className={styles.actionGrid} role="group" aria-label="In-game actions">
            <button type="button" className={styles.controlButton}>Check</button>
            <button type="button" className={styles.controlButton}>Call</button>
            <button type="button" className={styles.controlButton}>Raise</button>
            <button type="button" className={styles.controlButton}>Fold</button>
          </div>
        )}
        {activeTab === "money" && (
          <div className={styles.actionGrid} role="group" aria-label="Monetary actions">
            <button type="button" className={styles.controlButton}>Buy-in</button>
            <button type="button" className={styles.controlButton}>Transfer</button>
            <button type="button" className={styles.controlButton}>Tip</button>
          </div>
        )}
        {activeTab === "other" && (
          <div className={styles.actionGrid} role="group" aria-label="Other player actions">
            <button type="button" className={styles.controlButton}>AFK</button>
            <button type="button" className={styles.controlButton}>Leave table</button>
            <button
              type="button"
              className={`${styles.controlButton} ${styles.unseatButton}`}
              disabled={loading}
              onClick={handleUnseat}
            >
              {loading ? "Leaving..." : "Unseat"}
            </button>
          </div>
        )}
      </div>
      <div className={styles.sideButtons} role="tablist" aria-label="Player action categories">
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === "game"}
          aria-controls={`player-controls-${player.id}`}
          className={`${styles.sideButton} ${activeTab === "game" ? styles.activeTab : ""}`}
          onClick={() => selectTab("game")}
        >
          A
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === "money"}
          aria-controls={`player-controls-${player.id}`}
          className={`${styles.sideButton} ${activeTab === "money" ? styles.activeTab : ""}`}
          onClick={() => selectTab("money")}
        >
          B
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === "other"}
          aria-controls={`player-controls-${player.id}`}
          className={`${styles.sideButton} ${activeTab === "other" ? styles.activeTab : ""}`}
          onClick={() => selectTab("other")}
        >
          C
        </button>
      </div>
    </section>
  );
}
