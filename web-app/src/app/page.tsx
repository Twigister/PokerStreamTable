"use client";

import Game from "./components/game";
import PlayersMenu from "./components/players_menu";
import styles from "./page.module.css";
import { PlayerProfileUpdate, PlayerUnseatUpdate, SeatedPlayerUpdate } from "./types";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import React, { useState } from "react";

export default function Home() {
  const [updatedPlayer, setUpdatedPlayer] = useState<PlayerProfileUpdate | null>(null);
  const [seatedPlayer, setSeatedPlayer] = useState<SeatedPlayerUpdate | null>(null);
  const [unseatedPlayer, setUnseatedPlayer] = useState<PlayerUnseatUpdate | null>(null);

  return (
    <DndProvider backend={HTML5Backend}>
      <div className={styles.app}>
        <header className={styles.header}>
          <div className={styles.header_links}>
            <PlayersMenu
              onPlayerUpdated={setUpdatedPlayer}
              seatedPlayer={seatedPlayer}
              unseatedPlayer={unseatedPlayer}
            />
            <span>Link 2</span>
            <span>Link 3</span>
          </div>
          <button className={styles.settings}></button>
        </header>
        <Game
          updatedPlayer={updatedPlayer}
          onPlayerSeated={setSeatedPlayer}
          onPlayerUnseated={setUnseatedPlayer}
        />
        <footer className={styles.footer}>
          On touche le fond...
        </footer>
      </div>
    </DndProvider>
  );
}
