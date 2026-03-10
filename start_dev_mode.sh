#!/usr/bin/env bash
# Summoner Wars Tracker – development mode: backend (FastAPI) + frontend (Vite)

# Don't exit on first failure so we can start both and then wait
set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null && echo -e "${GREEN}Backend stopped${NC}"
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null && echo -e "${GREEN}Frontend stopped${NC}"
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Summoner Wars Tracker – Dev Mode${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}Configuration:${NC}"
echo -e "  Project root:  $PROJECT_ROOT"
echo -e "  Frontend:      $FRONTEND_DIR"
echo -e "  Database:      $PROJECT_ROOT/database.db"

# Check for required tools
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: 'uv' is not installed${NC}"
    echo "  Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: 'node' is not installed${NC}"
    exit 1
fi
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: 'npm' is not installed${NC}"
    exit 1
fi

# Start backend (must run from PROJECT_ROOT so uv finds the project)
echo -e "\n${GREEN}Starting Backend...${NC}"
echo -e "  Port: 8000"
(
    cd "$PROJECT_ROOT" && exec uv run uvicorn summoner_war_webapp.main:app --reload --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!
echo -e "  PID: $BACKEND_PID"

echo -e "  ${YELLOW}Waiting for backend...${NC}"
for i in $(seq 1 30); do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "  ${GREEN}Backend ready${NC}"
        break
    fi
    sleep 1
done
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "  ${RED}Backend did not become ready. Check output above.${NC}"
fi

# Start frontend
echo -e "\n${GREEN}Starting Frontend...${NC}"
echo -e "  Port: 5173 (Vite)"
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "  ${YELLOW}Installing dependencies...${NC}"
    (cd "$FRONTEND_DIR" && npm install)
fi
(
    cd "$FRONTEND_DIR" && exec npm run dev
) &
FRONTEND_PID=$!
echo -e "  PID: $FRONTEND_PID"

echo -e "  ${YELLOW}Waiting for frontend...${NC}"
for i in $(seq 1 30); do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "  ${GREEN}Frontend ready${NC}"
        break
    fi
    sleep 1
done
if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "  ${YELLOW}Frontend may still be starting...${NC}"
fi

# Try to get LAN IP for access from other devices on WiFi
LAN_IP=""
if command -v ipconfig &> /dev/null; then
  LAN_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)
elif command -v hostname &> /dev/null; then
  LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
fi

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Dev environment running${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e ""
echo -e "  ${YELLOW}This machine:${NC}"
echo -e "    App:        http://localhost:5173"
echo -e "    Backend:    http://localhost:8000"
echo -e "    API docs:   http://localhost:8000/docs"
if [ -n "$LAN_IP" ]; then
  echo -e "  ${YELLOW}On your WiFi (other devices):${NC}"
  echo -e "    App:        http://${LAN_IP}:5173"
  echo -e "    Backend:    http://${LAN_IP}:8000"
fi
echo -e ""
echo -e "  Press ${RED}Ctrl+C${NC} to stop both services"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Block until one of the processes exits (or Ctrl+C triggers cleanup)
wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo -e "\n${YELLOW}One of the services exited. Stopping...${NC}"
cleanup
