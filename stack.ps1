param (
    [string]$Command = "up"
)

function Create-Network {
    docker network create shared-network 2>$null
}

switch ($Command) {
    "network" {
        Create-Network
    }
    "build" {
        docker compose build
    }
    "up" {
        Create-Network
        docker compose up -d
    }
    "down" {
        docker compose down
    }
    "clean" {
        docker compose down -v
        docker network rm shared-network 2>$null
    }
    "restart" {
        docker compose down
        Create-Network
        docker compose up -d
    }
    "logs" {
        docker compose logs -f
    }
    default {
        Write-Host "Usage: .\stack.ps1 [network|build|up|down|clean|restart|logs]"
    }
}
