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
    m, dict_d = score(gs_file, system_file)
    print(f"P=\t{m[0] * 100:.1f}%")
    print(f"R=\t{m[1] * 100:.1f}%")
    print(f"F1=\t{m[2] * 100:.1f}%")
    print(f"C=\t{m[3] * 100:.1f}%")
    return dict_d


def score(gs, system):
    # Read the input files.
    gs_map = {}
    read_file(gs, gs_map)
    system_map = {}
    read_file(system, system_map)
    dict_d = {}
    # Count how many good and bad answers the system gives.
    ok = 0
    notok = 0
    extras = 0
    for key in gs_map.keys():
        dict_d[key] = -1
    for key in system_map.keys():
        if key not in gs_map:
            extras += 1
            continue
        for answer in system_map[key]:
            if answer in gs_map[key]:
                ok += 1
                dict_d[key] = 1
            elif answer != "<unk>":
                notok += 1
                dict_d[key] = 0


    print(f"Correct Tags: {ok}\n"
          f"Incorrect Tags: {notok}\n"
          f"Tags not in Gold: {extras}\n"
          f"Total Tags: {ok + notok + extras}")
    # Compute precision, recall and f1 scores.
    m = [0.0, 0.0, 0.0, 0.0]
    print(len(gs_map))
    if ok + notok != 0:
        m[0] = ok / (ok + notok)
    if len(gs_map) != 0:
        m[1] = ok / len(gs_map)
    if m[0] + m[1] != 0.0:
        m[2] = (2 * m[0] * m[1]) / (m[0] + m[1])
    if len(gs_map) != 0:
        m[3] = (ok + notok) / len(gs_map)
    return m, dict_d


def read_file(file, map):
    with open(file, 'r') as f:
        cnt = 0
        for line in f:
            # print(line)
            cnt += 1
            ll = line.strip().split(" ")
            if len(ll) < 2:
                print(f"line number {cnt} not complete: {line.strip()}")
                continue
            if ll[0] not in map:
                map[ll[0]] = set()
            # else:
            #     print(int(ll[0][6:9])-1,int(ll[0][-3:])-1)
            for i in range(1, len(ll)):
                map[ll[0]].add(ll[i])
