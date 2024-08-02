import os

def calculate_scores(gs_file, system_file):

    # Check if the input files exist.
    if not os.path.exists(gs_file):
        print(f"Gold standard file '{gs_file}' does not exist.")
        return
    if not os.path.exists(system_file):
        print(f"System file '{system_file}' does not exist.")
        return

    # Compute measures.
    m = score(gs_file, system_file)
    print(f"P=\t{m[0] * 100:.1f}%")
    print(f"R=\t{m[1] * 100:.1f}%")
    print(f"F1=\t{m[2] * 100:.1f}%")

def score(gs, system):
    # Read the input files.
    gs_map = {}
    read_file(gs, gs_map)
    system_map = {}
    read_file(system, system_map)

    # Count how many good and bad answers the system gives.
    ok = 0
    notok = 0
    extras = 0
    for key in system_map.keys():
        if key not in gs_map:
            extras += 1
            continue
        for answer in system_map[key]:
            if answer in gs_map[key]:
                ok += 1
            else:
                notok += 1


    print(f"\nCorrect Tags: {ok}\nIncorrect Tags: {notok}\nTags not in Gold: {extras}\nTotal Tags: {ok+notok+extras}")
    # Compute precision, recall and f1 scores.
    m = [0.0, 0.0, 0.0]
    if ok + notok != 0:
        m[0] = ok / (ok + notok)
    if len(gs_map) != 0:
        m[1] = ok / len(gs_map)
    if m[0] + m[1] != 0.0:
        m[2] = (2 * m[0] * m[1]) / (m[0] + m[1])
    return m

def read_file(file, map):
    with open(file, 'r') as f:
        cnt = 0
        for line in f:
            cnt += 1
            ll = line.strip().split(" ")
            if len(ll) < 2:
                print(f"line number {cnt} not complete: {line.strip()}")
                continue
            if ll[0] not in map:
                map[ll[0]] = set()
            for i in range(1, len(ll)):
                map[ll[0]].add(ll[i])


