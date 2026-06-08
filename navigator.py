import heapq
GRAPH = {
    "宿舍": {"图书馆": 200, "第一食堂": 300, "校医院": 500},
    "图书馆": {"宿舍": 200, "第一食堂": 200, "超市": 200, "校医院": 300, "教学楼": 200},
    "第一食堂": {"宿舍": 300, "图书馆": 200, "操场": 300},
    "操场": {"第一食堂": 300, "教学楼": 200, "实验楼": 500},
    "教学楼": {"图书馆": 200, "操场": 200, "体育馆": 200, "超市": 300, "实验楼": 200},
    "体育馆": {"教学楼": 200, "行政楼": 200},
    "行政楼": {"体育馆": 200, "超市": 200, "第二食堂": 200, "实验楼": 300},
    "超市": {"图书馆": 200, "教学楼": 300, "校医院": 200, "行政楼": 200},
    "校医院": {"宿舍": 500, "图书馆": 300, "超市": 200},
    "实验楼": {"操场": 500, "教学楼": 200, "行政楼": 300},
    "第二食堂": {"行政楼": 200, "快递站": 200},
    "快递站": {"第二食堂": 200}
}

POS = {
    "宿舍": (80, 220),
    "第一食堂": (240, 180),
    "图书馆": (240, 240),
    "操场": (440, 180),
    "教学楼": (440, 240),
    "实验楼": (680, 240),
    "校医院": (120, 380),
    "超市": (320, 380),
    "体育馆": (440, 320),
    "行政楼": (440, 380),
    "第二食堂": (580, 380),
    "快递站": (700, 380)
}




def dfs(graph, start, end):
    stack = [start]
    visited = set()
    parent = {}
    steps = []

    steps.append((f"[初始化] 把起点「{start}」压入栈", "init", start, None))

    while stack:
        cur = stack.pop()

        if cur in visited:
            continue

        visited.add(cur)
        steps.append((f"[访问] 弹出「{cur}」，标记为已访问。栈内: {stack}", "visit", cur, None))

        if cur == end:
            path = []
            p = cur
            while p is not None:
                path.append(p)
                p = parent.get(p)
            path.reverse()
            steps.append((f"[完成] 找到目标「{end}」！路径: {' → '.join(path)}（DFS 不保证最短）",
                          "found", cur, path))
            return steps, path

        for nb in sorted(graph[cur].keys(), reverse=True):
            if nb not in visited:
                stack.append(nb)
                parent[nb] = cur
                steps.append((f"[探索] 从「{cur}」发现邻居「{nb}」，压入栈", "explore", nb, (cur, nb)))

    steps.append((f"[结束] 栈空，没有找到通往「{end}」的路径", "finish", None, None))
    return steps, None

def bfs(graph, start, end):
    queue = [start]
    visited = {start}
    parent = {}
    steps = []

    steps.append((f"[初始化] 把起点「{start}」入队并标记已访问", "init", start, None))

    while queue:
        cur = queue.pop(0)

        steps.append((f"[访问] 出队「{cur}」。队列: {queue}", "visit", cur, None))

        if cur == end:
            path = []
            p = cur
            while p is not None:
                path.append(p)
                p = parent.get(p)
            path.reverse()
            steps.append((f"[完成] 找到目标「{end}」！路径: {' → '.join(path)}（BFS 保证边数最少）",
                          "found", cur, path))
            return steps, path

        for nb in graph[cur]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                parent[nb] = cur
                steps.append((f"[探索] 从「{cur}」发现邻居「{nb}」，入队尾", "explore", nb, (cur, nb)))

    steps.append((f"[结束] 队列空，没有找到通往「{end}」的路径", "finish", None, None))
    return steps, None

def dijkstra(graph, start, end):
    INF = float("inf")
    dist = {node: INF for node in graph}
    dist[start] = 0
    visited = set()
    parent = {}
    heap = [(0, start)]
    steps = []

    steps.append((f"[初始化] 所有节点距离=∞，起点「{start}」距离=0。堆: [(0, {start})]",
                  "init", start, None))

    while heap:
        d, cur = heapq.heappop(heap)

        if cur in visited:
            steps.append((f"[跳过] 「{cur}」已通过更短路径访问过，忽略", "skip", cur, None))
            continue

        visited.add(cur)
        steps.append((f"[确定] 取出「{cur}」，距离={d}m，这是到「{cur}」的最短距离",
                      "visit", cur, None))

        if cur == end:
            path = []
            p = cur
            while p is not None:
                path.append(p)
                p = parent.get(p)
            path.reverse()
            steps.append((f"[完成] 最短路径: {' → '.join(path)}，总距离={dist[end]}m",
                          "found", cur, path))
            return steps, path

        for nb, w in graph[cur].items():
            new_d = dist[cur] + w
            if new_d < dist[nb]:
                dist[nb] = new_d
                parent[nb] = cur
                heapq.heappush(heap, (new_d, nb))
                steps.append((f"[松弛] 「{cur}」→「{nb}」: 新距离={new_d}m < 旧距离，更新！",
                              "relax", nb, (cur, nb)))
            else:
                steps.append((f"[检查] 「{cur}」→「{nb}」: 新距离={new_d}m ≥ 旧距离，不更新",
                              "check", nb, (cur, nb)))

    steps.append((f"[结束] 堆空，「{end}」不可达", "finish", None, None))
    return steps, None


def console_test():
      print("算法: 1=DFS  2=BFS  3=Dijkstra")
      algo = input("请输入编号: ")
      start = input("请输入起点: ")
      end = input("请输入终点: ")

      func = {"1": dfs, "2": bfs, "3": dijkstra}.get(algo)
      if func is None:
          print("编号不对")
          exit()

      steps, path = func(GRAPH, start, end)

      for desc, _, _, _ in steps:
          print(desc)

      if path:
          print(f"\n路径: {' →'.join(path)}")
      else:
          print("\n没找到")




if __name__ == "__main__":
      import tkinter as tk
      from tkinter import ttk

      root = tk.Tk()
      root.title("校园地图导航")
      root.geometry("1050x550")

      main = tk.Frame(root)
      main.pack(fill=tk.BOTH, expand=True)

      canvas = tk.Canvas(main, width=720, height=520, bg="white")
      canvas.pack(side=tk.LEFT)

      panel = tk.Frame(main, width=320)
      panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=8)

      tk.Label(panel, text="选择算法", font=("微软雅黑", 11, "bold")).pack(pady=(8, 4))
      algo_var = tk.StringVar(value="DFS")
      tk.Radiobutton(panel, text="DFS 深度优先", variable=algo_var, value="DFS",
                     font=("微软雅黑", 9)).pack(anchor=tk.W, padx=15)
      tk.Radiobutton(panel, text="BFS 广度优先", variable=algo_var, value="BFS",
                     font=("微软雅黑", 9)).pack(anchor=tk.W, padx=15)
      tk.Radiobutton(panel, text="Dijkstra 最短路径", variable=algo_var, value="Dijkstra",
                     font=("微软雅黑", 9)).pack(anchor=tk.W, padx=15)

      tk.Label(panel, text="起点 / 终点", font=("微软雅黑", 11, "bold")).pack(pady=(12, 4))
      names = list(POS.keys())
      tk.Label(panel, text="起点:", font=("微软雅黑", 9)).pack(anchor=tk.W, padx=15)
      start_var = tk.StringVar(value="宿舍")
      ttk.Combobox(panel, textvariable=start_var, values=names,
                   state="readonly", width=12).pack(padx=15, pady=(0, 6))
      tk.Label(panel, text="终点:", font=("微软雅黑", 9)).pack(anchor=tk.W, padx=15)
      end_var = tk.StringVar(value="快递站")
      ttk.Combobox(panel, textvariable=end_var, values=names,
                   state="readonly", width=12).pack(padx=15, pady=(0, 6))

      info_text = tk.Text(panel, font=("微软雅黑", 9), wrap=tk.WORD,
                          height=6, width=38, fg="#333333", bg="#F5F5F5",
                          relief=tk.FLAT, padx=6, pady=4)
      info_text.pack(pady=8, padx=12, fill=tk.X)
      info_text.insert("1.0", "请选择算法和起止点")

      def draw_map():
          drawn = set()
          for a, neighbors in GRAPH.items():
              x1, y1 = POS[a]
              for b, w in neighbors.items():
                  k = tuple(sorted((a, b)))
                  if k in drawn:
                      continue
                  drawn.add(k)
                  x2, y2 = POS[b]
                  canvas.create_line(x1, y1, x2, y2, fill="#AAAAAA", width=1.5,
                                     tags=f"e_{k[0]}_{k[1]}")
                  mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                  canvas.create_text(mx + 10, my - 8, text=str(w) + "m",
                                     fill="#999999", font=("", 7))
          R = 18
          for name, (x, y) in POS.items():
              canvas.create_oval(x - R, y - R, x + R, y + R,
                                 fill="#E8E8E8", outline="#999999", width=1.5,
                                 tags=f"n_{name}")
              canvas.create_text(x, y, text=name, font=("微软雅黑", 7, "bold"))

      draw_map()

      def reset_map():
          for name in POS:
              canvas.itemconfig(f"n_{name}", fill="#E8E8E8")
          for a, neighbors in GRAPH.items():
              for b in neighbors:
                  k = tuple(sorted((a, b)))
                  canvas.itemconfig(f"e_{k[0]}_{k[1]}", fill="#AAAAAA", width=1.5)

      def on_start():
          reset_map()

          algo = algo_var.get()
          start = start_var.get()
          end = end_var.get()

          if algo == "DFS":
              steps, path = dfs(GRAPH, start, end)
          elif algo == "BFS":
              steps, path = bfs(GRAPH, start, end)
          else:
              steps, path = dijkstra(GRAPH, start, end)

          canvas.itemconfig(f"n_{start}", fill="#4CAF50")
          canvas.itemconfig(f"n_{end}", fill="#FF6B6B")

          visited_nodes = set()
          idx = 0

          def play_step():
              nonlocal idx
              if idx >= len(steps):
                  return

              desc, typ, node, extra = steps[idx]
              info_text.delete("1.0", tk.END)
              info_text.insert("1.0", f"[{idx+1}/{len(steps)}] {desc}")

              if typ in ("init", "visit") and node:
                  visited_nodes.add(node)
                  for n in visited_nodes:
                      canvas.itemconfig(f"n_{n}", fill="#4A90D9")
                  canvas.itemconfig(f"n_{node}", fill="#FFD93D")

              if typ in ("explore", "relax") and node:
                  visited_nodes.add(node)
                  for n in visited_nodes:
                      canvas.itemconfig(f"n_{n}", fill="#4A90D9")
                  canvas.itemconfig(f"n_{node}", fill="#FFD93D")

              if typ == "found" and extra:
                  for i in range(len(extra) - 1):
                      k = tuple(sorted((extra[i], extra[i+1])))
                      canvas.itemconfig(f"e_{k[0]}_{k[1]}", fill="#9B59B6", width=3)
                  for n in extra:
                      canvas.itemconfig(f"n_{n}", fill="#9B59B6")

              idx += 1
              root.after(500, play_step)

          play_step()

      tk.Button(panel, text="▶开始搜索", command=on_start,
                font=("微软雅黑", 11, "bold"), bg="#4CAF50", fg="white",
                padx=10, pady=4).pack(pady=8)

      root.mainloop()
