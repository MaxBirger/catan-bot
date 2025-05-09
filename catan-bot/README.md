# Catan Bot

This project implements a full Python-based simulation of the board game *Catan*, along with two autonomous bots that aim to play the game optimally:

- **MCTS Bot**: Uses Monte Carlo Tree Search to simulate possible futures and select actions with the highest win potential.
- **Reinforcement Learning Bot**: Trained to learn optimal strategies using feedback from simulated games.

The goal is to compare these approaches in terms of gameplay effectiveness and decision quality.

---

## Features

- Full Catan game engine, including:
  - Board setup, resource distribution, robber mechanics
  - Turn-based actions: build, trade, play development cards
  - Longest Road and Largest Army scoring
- Bot-ready Gym-style environment
- Modular, testable code structure
- Support for AI-vs-AI tournaments

---

## 📁 Project Structure

