import tkinter as tk
import random

W, H, PW, R, SP = 600, 500, 100, 8, 5          # board, paddle width, ball radius, speed
COLORS = ["#EF4444", "#F97316", "#FACC15", "#22C55E", "#38BDF8"]
s = {}                                          # game state

root = tk.Tk()
root.title("BRICK BREAKER")
root.resizable(False, False)
root.configure(bg="#172554")
tk.Label(root, text="BRICK BREAKER", font=("Arial Black", 22),
         bg="#172554", fg="white").pack(pady=10)
info = tk.Frame(root, bg="#172554")
info.pack()
score_lbl = tk.Label(info, font=("Arial", 16, "bold"), bg="#172554", fg="#FACC15")
lives_lbl = tk.Label(info, font=("Arial", 16, "bold"), bg="#172554", fg="#F87171")
score_lbl.pack(side="left", padx=25)
lives_lbl.pack(side="left", padx=25)
cv = tk.Canvas(root, width=W, height=H, bg="#0F172A",
               highlightthickness=2, highlightbackground="#38BDF8")
cv.pack(padx=20, pady=10)
bf = tk.Frame(root, bg="#172554")
bf.pack(pady=10)
tk.Button(bf, text="RESTART GAME", font=("Arial", 12, "bold"), bg="#22C55E",
          command=lambda: restart()).pack(side="left", padx=10)
tk.Button(bf, text="EXIT", font=("Arial", 12, "bold"), bg="#EF4444", fg="white",
          command=root.destroy).pack(side="left", padx=10)


def restart():
    s.update(score=0, lives=3, px=(W - PW) // 2,
             bricks=[(c * 60, 50 + r * 24, r) for r in range(5) for c in range(10)])
    reset_ball()


def reset_ball():
    s.update(state="ready", bx=s["px"] + PW // 2, by=H - 40 - R, vx=0, vy=0)


def move(x):
    if s["state"] in ("over", "won"):
        return
    s["px"] = max(0, min(W - PW, x))
    if s["state"] == "ready":
        s["bx"] = s["px"] + PW // 2


def launch(e=None):
    if s["state"] == "ready":
        s.update(state="playing", vx=random.choice([-3, 3]), vy=-SP)


def step():
    s["bx"] += s["vx"]
    s["by"] += s["vy"]
    x, y = s["bx"], s["by"]
    if x < R or x > W - R:                                   # side walls
        s["vx"] *= -1
        s["bx"] = x = max(R, min(W - R, x))
    if y < R:                                                # top wall
        s["vy"] = abs(s["vy"])
    px = s["px"]
    if s["vy"] > 0 and H - 40 <= y + R <= H - 20 and px - R <= x <= px + PW + R:   # paddle
        s["vx"] = (x - px - PW / 2) / (PW / 2) * SP * 1.2
        s["vy"], s["by"] = -SP, H - 40 - R
    for b in s["bricks"]:                                    # bricks
        bx, by, r = b
        if bx - R <= x <= bx + 60 + R and by - R <= y <= by + 24 + R:
            s["bricks"].remove(b)
            s["score"] += (5 - r) * 10
            if min(x + R - bx, bx + 60 - x + R) < min(y + R - by, by + 24 - y + R):
                s["vx"] *= -1
            else:
                s["vy"] *= -1
            break
    if not s["bricks"]:
        s["state"] = "won"
    elif y - R > H:                                          # ball lost
        s["lives"] -= 1
        reset_ball() if s["lives"] else s.update(state="over")


def draw():
    cv.delete("all")
    score_lbl.config(text=f"SCORE: {s['score']}")
    lives_lbl.config(text=f"LIVES: {s['lives']}")
    for x, y, r in s["bricks"]:
        cv.create_rectangle(x + 1, y + 1, x + 59, y + 23, fill=COLORS[r], outline="#0F172A")
    cv.create_rectangle(s["px"], H - 40, s["px"] + PW, H - 26,
                        fill="#86EFAC", outline="#14532D")
    cv.create_oval(s["bx"] - R, s["by"] - R, s["bx"] + R, s["by"] + R,
                   fill="white", outline="")
    if s["state"] == "ready":
        cv.create_text(W // 2, H // 2 + 60, fill="#94A3B8", font=("Arial", 13),
                       text="Move: Mouse / Arrow keys     Launch: SPACE")
    elif s["state"] in ("over", "won"):
        cv.create_rectangle(130, H // 2 - 70, 470, H // 2 + 70,
                            fill="#172554", outline="#38BDF8", width=2)
        cv.create_text(W // 2, H // 2 - 25, font=("Arial Black", 27),
                       text="GAME OVER" if s["state"] == "over" else "YOU WIN!",
                       fill="#EF4444" if s["state"] == "over" else "#FACC15")
        cv.create_text(W // 2, H // 2 + 25, text=f"Final Score: {s['score']}",
                       font=("Arial", 18), fill="white")


def loop():
    if s["state"] == "playing":
        step()
    draw()
    root.after(16, loop)


root.bind("<Left>", lambda e: move(s["px"] - 28))
root.bind("<Right>", lambda e: move(s["px"] + 28))
root.bind("<space>", launch)
cv.bind("<Motion>", lambda e: move(e.x - PW // 2))
restart()
loop()
root.mainloop()
