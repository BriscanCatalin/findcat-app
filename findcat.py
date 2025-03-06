import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
GRID_SIZE = 100  # Dimensiunea grilei (poate fi ajustată)

class CatGame:
    def __init__(self):
        while True:
            self.cat_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            self.player_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if self.cat_position != self.player_position:
                break

    def get_distance(self):
        px, py = self.player_position
        cx, cy = self.cat_position
        return abs(px - cx) + abs(py - cy)

    def move(self, direction):
        x, y = self.player_position

        # Handle custom "to_x_y" direction for direct movement
        if direction.startswith("to_"):
            parts = direction.split("_")
            if len(parts) == 3 and parts[0] == "to":
                try:
                    new_x, new_y = int(parts[1]), int(parts[2])
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                        x, y = new_x, new_y  # Set new position directly
                except (ValueError, IndexError):
                    pass  # Ignore invalid directions

        # Handle standard directions (north, south, west, east)
        elif direction == "north" and x > 0:
            x -= 1
        elif direction == "south" and x < GRID_SIZE - 1:
            x += 1
        elif direction == "west" and y > 0:
            y -= 1
        elif direction == "east" and y < GRID_SIZE - 1:
            y += 1

        self.player_position = (x, y)

        # Check if the player found the cat
        if self.player_position == self.cat_position:
            return {"message": "🎉 You found the cat! 🐱", "player_position": self.player_position}

        # Provide hints based on distance
        distance = self.get_distance()
        if distance <= 4:
            hint = "🎧 I hear purring nearby! 🐾"
        elif distance <= 8:
            hint = "🔥 Getting warmer..."
        elif distance <= 12:
            hint = "🌬️ It's a bit chilly."
        elif distance <= 20:
            hint = "🥶 It's freezing cold!"
        else:
            hint = "🔇 It's quiet... The cat is far away."

        return {"message": hint, "player_position": self.player_position}

game = CatGame()

@app.route('/')
def index():
    return render_template('index.html', grid_size=GRID_SIZE)

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    result = game.move(direction)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)