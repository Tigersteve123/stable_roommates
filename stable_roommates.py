'''Code from https://github.com/jmoh3/stable_roommates/tree/master, fixed with ChatGPT'''

class StableRoommates:
    def __init__(self, preferences):
        self.preferences = preferences
        self.num_individuals = len(preferences)
        self.rank = self.get_ranking_matrix(preferences)
        self.first = [0 for _ in range(self.num_individuals)]
        self.last = [len(preference) for preference in preferences]

    def get_ranking_matrix(self, preferences):
        rank = [[None for _ in range(len(preferences))] for _ in range(len(preferences))]
        for i in range(len(preferences)):
            for j in range(len(preferences[i])):
                rank[i][preferences[i][j]] = j
        return rank

    def stable_roommates_phase_1(self):
        proposal = [None for _ in range(self.num_individuals)]
        to_process = [i for i in range(self.num_individuals)]

        while to_process:
            i = to_process.pop(0)
            while self.preferences[i][self.first[i]] is None:
                self.first[i] += 1
            
            top_pick = self.preferences[i][self.first[i]]

            if proposal[top_pick] is None:
                proposal[top_pick] = i
                match_rank = self.preferences[top_pick].index(i)

                for x in range(match_rank + 1, self.last[top_pick]):
                    reject = self.preferences[top_pick][x]
                    if reject is not None and self.rank[reject][top_pick] is not None:
                        self.preferences[reject][self.rank[reject][top_pick]] = None

                self.last[top_pick] = match_rank
            
            else:
                curr_match_idx = self.rank[top_pick][proposal[top_pick]]
                potential_match_idx = self.rank[top_pick][i]
                
                if curr_match_idx < potential_match_idx:
                    self.preferences[top_pick][potential_match_idx] = None
                    self.first[i] += 1
                
                else:
                    self.preferences[top_pick][curr_match_idx] = None
                    top_pick_idx = self.rank[proposal[top_pick]][top_pick]
                    self.preferences[proposal[top_pick]][top_pick_idx] = None
                    to_process.insert(0, proposal[top_pick])
                    proposal[top_pick] = i
                    self.last[top_pick] = potential_match_idx

    def find_second_favorite(self, i):
        count = 0
        for j in range(self.first[i], self.last[i] + 1):
            if self.preferences[i][j] is not None:
                count += 1
            elif count == 0:
                self.first[i] += 1
            if count == 2:
                return self.preferences[i][j]
        return None

    def find_rotation(self, i, p, q):
        second_favorite = self.find_second_favorite(p[i])
        next_p = self.preferences[second_favorite][self.last[second_favorite]]
        
        if next_p in p:
            j = p.index(next_p)
            q[j] = second_favorite
            return p[j:], q[j:]

        q.append(second_favorite)
        p.append(next_p)
        return self.find_rotation(i + 1, p, q)

    def eliminate_rotation(self, p, q):
        for i in range(len(p)):
            self.preferences[p[i]][self.rank[p[i]][q[i]]] = None
            for j in range(self.rank[q[i]][p[i - 1]] + 1, self.last[q[i]]):
                reject = self.rank[q[i]].index(j)
                self.preferences[reject][self.rank[reject][q[i]]] = None
            self.last[q[i]] = self.rank[q[i]][p[i - 1]]

    def stable_roommates_phase_2(self):
        while True:
            p, q = None, None
            for i in range(self.num_individuals):
                if self.last[i] - self.first[i] > 0 and self.find_second_favorite(i) is not None:
                    p, q = self.find_rotation(0, [i], [None])
                    break
            
            if not p and not q:
                return
            
            self.eliminate_rotation(p, q)

    def match_roommates(self):
        self.stable_roommates_phase_1()
        self.stable_roommates_phase_2()

        matches = []
        visited = set()
        
        for i in range(len(self.preferences)):
            if i not in visited:
                pair = (i, self.preferences[i][self.last[i]])
                visited.add(self.last[i])
                matches.append(pair)
        
        return matches


# Example usage:
'''preferences = [[1, 2, 3], [0, 3, 2], [1, 3, 0], [1, 2, 0]]
sr = StableRoommates(preferences)
print(sr.match_roommates())'''

