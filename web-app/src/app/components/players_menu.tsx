"use client";

import React, { useEffect, useState } from "react";
import { useDrag, useDragLayer } from "react-dnd";
import {
  PLAYER_DRAG_TYPE,
  PlayerProfileUpdate,
  PlayerUnseatUpdate,
  SeatedPlayerUpdate,
} from "../types";
import styles from "./players_menu.module.css";

type RegisteredPlayer = PlayerProfileUpdate & {
  id: number;
  table_id: number | null;
  created_at: string;
  seat_number: number | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

function PlayerDragLayer() {
  const { item, itemType, currentOffset, isDragging } = useDragLayer((monitor) => ({
    item: monitor.getItem() as RegisteredPlayer | null,
    itemType: monitor.getItemType(),
    currentOffset: monitor.getSourceClientOffset(),
    isDragging: monitor.isDragging(),
  }));

  if (!isDragging || itemType !== PLAYER_DRAG_TYPE || !item || !currentOffset) {
    return null;
  }

  return (
    <div
      className={styles.drag_layer}
      style={{
        transform: `translate(${currentOffset.x + 12}px, ${currentOffset.y + 12}px)`,
      }}
    >
      <img
        className={styles.drag_layer_picture}
        src={item.image_url || "/default_avatar.webp"}
        alt=""
      />
      <span>{item.name}</span>
    </div>
  );
}

export default function PlayersMenu({ onPlayerUpdated, seatedPlayer, unseatedPlayer }: {
  onPlayerUpdated: (player: PlayerProfileUpdate) => void;
  seatedPlayer: SeatedPlayerUpdate | null;
  unseatedPlayer: PlayerUnseatUpdate | null;
}) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [registeredPlayers, setRegisteredPlayers] = useState<RegisteredPlayer[]>([]);
  const [isLoadingPlayers, setIsLoadingPlayers] = useState(false);
  const [isRegisteringPlayer, setIsRegisteringPlayer] = useState(false);
  const [openPlayerOptions, setOpenPlayerOptions] = useState<number | null>(null);
  const [editingPlayerId, setEditingPlayerId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const [editImageUrl, setEditImageUrl] = useState("");
  const [isSavingPlayer, setIsSavingPlayer] = useState(false);
  const [playersError, setPlayersError] = useState("");
  const [draggingPlayer, setDraggingPlayer] = useState<RegisteredPlayer | null>(null);

  const filteredPlayers = registeredPlayers.filter((player) =>
    player.name.toLocaleLowerCase().includes(searchTerm.trim().toLocaleLowerCase()),
  );

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
      type: PLAYER_DRAG_TYPE,
      item: player,
      canDrag: player.seat_number === null,
      collect: (monitor) => ({ isDragging: monitor.isDragging() }),
    }), [player]);

    useEffect(() => {
      if (isDragging) {
        setDraggingPlayer(player);
        setIsMenuOpen(false);
      } else if (draggingPlayer?.id === player.id) {
        setDraggingPlayer(null);
      }
    }, [isDragging, player, draggingPlayer?.id]);

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
      {(isMenuOpen || draggingPlayer) && (
        <div
          id="players-menu"
          className={`${styles.players_panel} ${draggingPlayer ? styles.drag_source_hidden : ""}`}
        >
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
            <label className={styles.search_field} htmlFor="player-search">
              Search players
            </label>
            <input
              id="player-search"
              className={styles.search_input}
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search by name"
              autoComplete="off"
            />
            {isLoadingPlayers ? (
              <p>Loading players...</p>
            ) : filteredPlayers.length > 0 ? (
              <ul>
                {filteredPlayers.map((player) => (
                  <DraggablePlayerRow key={player.id} player={player} />
                ))}
              </ul>
            ) : registeredPlayers.length > 0 ? (
              <p>No players match “{searchTerm}”.</p>
            ) : (
              <p>No players registered yet.</p>
            )}
            {playersError && <p className={styles.players_error}>{playersError}</p>}
          </div>
        </div>
      )}
      <PlayerDragLayer />
    </div>
  );
}
