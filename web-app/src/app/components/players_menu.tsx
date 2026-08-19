"use client";

import React, { useEffect, useState } from "react";
import { useDrag } from "react-dnd";
import { PlayerProfileUpdate, PlayerUnseatUpdate, SeatedPlayerUpdate } from "../types";
import styles from "./players_menu.module.css";

type RegisteredPlayer = PlayerProfileUpdate & {
  id: number;
  table_id: number | null;
  created_at: string;
  seat_number: number | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function PlayersMenu({ onPlayerUpdated, seatedPlayer, unseatedPlayer }: {
  onPlayerUpdated: (player: PlayerProfileUpdate) => void;
  seatedPlayer: SeatedPlayerUpdate | null;
  unseatedPlayer: PlayerUnseatUpdate | null;
}) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [registeredPlayers, setRegisteredPlayers] = useState<RegisteredPlayer[]>([]);
  const [isLoadingPlayers, setIsLoadingPlayers] = useState(false);
  const [isRegisteringPlayer, setIsRegisteringPlayer] = useState(false);
  const [openPlayerOptions, setOpenPlayerOptions] = useState<number | null>(null);
  const [editingPlayerId, setEditingPlayerId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const [editImageUrl, setEditImageUrl] = useState("");
  const [isSavingPlayer, setIsSavingPlayer] = useState(false);
  const [playersError, setPlayersError] = useState("");

  useEffect(() => {
    async function loadPlayers() {
      setIsLoadingPlayers(true);
      setPlayersError("");

      try {
        const response = await fetch(`${API_URL}/users/`);
        if (!response.ok) {
          throw new Error("Unable to load players.");
        }

        setRegisteredPlayers(await response.json());
      } catch {
        setPlayersError("The player service is unavailable.");
      } finally {
        setIsLoadingPlayers(false);
      }
    }

    loadPlayers();
  }, []);

  useEffect(() => {
    if (!seatedPlayer) {
      return;
    }

    setRegisteredPlayers((players) => players.map((player) =>
      player.id === seatedPlayer.id ? { ...player, ...seatedPlayer } : player,
    ));
  }, [seatedPlayer]);

  useEffect(() => {
    if (!unseatedPlayer) {
      return;
    }

    setRegisteredPlayers((players) => players.map((player) =>
      player.id === unseatedPlayer.id ? { ...player, table_id: null, seat_number: null } : player,
    ));
  }, [unseatedPlayer]);

  async function registerPlayer(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedName = playerName.trim();

    if (!trimmedName || isRegisteringPlayer) {
      return;
    }

    setIsRegisteringPlayer(true);
    setPlayersError("");

    try {
      const response = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: trimmedName, image_url: null }),
      });

      if (!response.ok) {
        throw new Error("Unable to register player.");
      }

      const registeredPlayer: RegisteredPlayer = await response.json();
      setRegisteredPlayers((players) => [...players, registeredPlayer]);
      setPlayerName("");
    } catch {
      setPlayersError("The player could not be registered.");
    } finally {
      setIsRegisteringPlayer(false);
    }
  }

  function startEditingPlayer(player: RegisteredPlayer) {
    setEditingPlayerId(player.id);
    setEditName(player.name);
    setEditImageUrl(player.image_url ?? "");
  }

  async function savePlayer(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedName = editName.trim();

    if (!trimmedName || editingPlayerId === null || isSavingPlayer) {
      return;
    }

    setIsSavingPlayer(true);
    setPlayersError("");

    try {
      const response = await fetch(`${API_URL}/users/${editingPlayerId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: trimmedName,
          image_url: editImageUrl.trim() || null,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to update player.");
      }

      const updatedPlayer: RegisteredPlayer = await response.json();
      setRegisteredPlayers((players) =>
        players.map((player) => player.id === updatedPlayer.id ? updatedPlayer : player),
      );
      onPlayerUpdated(updatedPlayer);
      setEditingPlayerId(null);
      setOpenPlayerOptions(null);
    } catch {
      setPlayersError("The player could not be updated.");
    } finally {
      setIsSavingPlayer(false);
    }
  }

  async function deletePlayer(playerId: number) {
    if (!window.confirm("Delete this player?")) {
      return;
    }

    setPlayersError("");

    try {
      const response = await fetch(`${API_URL}/users/${playerId}`, { method: "DELETE" });
      if (!response.ok) {
        throw new Error("Unable to delete player.");
      }

      setRegisteredPlayers((players) => players.filter((player) => player.id !== playerId));
      setOpenPlayerOptions(null);
    } catch {
      setPlayersError("The player could not be deleted.");
    }
  }

  function DraggablePlayerRow({ player }: { player: RegisteredPlayer }) {
    const [{ isDragging }, drag] = useDrag(() => ({
      type: "registered-player",
      item: player,
      canDrag: player.seat_number === null,
      collect: (monitor) => ({ isDragging: monitor.isDragging() }),
    }), [player]);

    return (
      <li
        ref={drag}
        key={player.id}
        className={`${styles.player_row} ${isDragging ? styles.dragging : ""}`}
        title={player.seat_number === null ? "Drag to an empty seat" : "Player is already seated"}
      >
        <img
          className={styles.player_picture}
          src={player.image_url || "/default_avatar.webp"}
          alt=""
        />
        <span className={styles.player_name}>{player.name}</span>
        {player.seat_number !== null && (
          <span className={styles.seated_label}>Seat {player.seat_number}</span>
        )}
        <div className={styles.player_options}>
          <button
            type="button"
            className={styles.options_trigger}
            aria-label={`Options for ${player.name}`}
            aria-expanded={openPlayerOptions === player.id}
            onClick={() => setOpenPlayerOptions((openId) => openId === player.id ? null : player.id)}
          >
            ⋮
          </button>
          {openPlayerOptions === player.id && (
            <div className={styles.options_panel}>
              {editingPlayerId === player.id ? (
                <form className={styles.edit_form} onSubmit={savePlayer}>
                  <label htmlFor={`edit-name-${player.id}`}>Name</label>
                  <input
                    id={`edit-name-${player.id}`}
                    type="text"
                    value={editName}
                    onChange={(event) => setEditName(event.target.value)}
                    maxLength={100}
                  />
                  <label htmlFor={`edit-image-${player.id}`}>Picture URL</label>
                  <input
                    id={`edit-image-${player.id}`}
                    type="url"
                    value={editImageUrl}
                    onChange={(event) => setEditImageUrl(event.target.value)}
                    placeholder="https://..."
                  />
                  <div className={styles.edit_actions}>
                    <button type="submit" disabled={isSavingPlayer}>
                      {isSavingPlayer ? "Saving..." : "Save"}
                    </button>
                    <button type="button" onClick={() => setEditingPlayerId(null)}>
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <button type="button" onClick={() => startEditingPlayer(player)}>
                    Edit player
                  </button>
                  {player.seat_number === null && (
                    <button
                      type="button"
                      className={styles.delete_action}
                      onClick={() => deletePlayer(player.id)}
                    >
                      Delete player
                    </button>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </li>
    );
  }

  return (
    <div className={styles.players_menu}>
      <button
        type="button"
        className={styles.players_trigger}
        aria-expanded={isMenuOpen}
        aria-controls="players-menu"
        onClick={() => setIsMenuOpen((isOpen) => !isOpen)}
      >
        Players ({registeredPlayers.length})
        <span aria-hidden="true">⌄</span>
      </button>
      {isMenuOpen && (
        <div id="players-menu" className={styles.players_panel}>
          <form className={styles.registration_form} onSubmit={registerPlayer}>
            <label htmlFor="player-name">Register a player</label>
            <div className={styles.registration_fields}>
              <input
                id="player-name"
                type="text"
                value={playerName}
                onChange={(event) => setPlayerName(event.target.value)}
                placeholder="Player name"
                maxLength={30}
              />
              <button type="submit" disabled={isRegisteringPlayer}>
                {isRegisteringPlayer ? "Adding..." : "Add"}
              </button>
            </div>
          </form>
          <div className={styles.registered_players}>
            <h2>Registered players</h2>
            {isLoadingPlayers ? (
              <p>Loading players...</p>
            ) : registeredPlayers.length > 0 ? (
              <ul>
                {registeredPlayers.map((player) => (
                  <DraggablePlayerRow key={player.id} player={player} />
                ))}
              </ul>
            ) : (
              <p>No players registered yet.</p>
            )}
            {playersError && <p className={styles.players_error}>{playersError}</p>}
          </div>
        </div>
      )}
    </div>
  );
}
