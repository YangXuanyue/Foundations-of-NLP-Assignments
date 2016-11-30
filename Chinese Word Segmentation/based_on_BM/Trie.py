class Trie:
    def __init__(self):
        self.size = 0
        self.next = []
        self.end = []
        self.root = self.create_new_node()

    def create_new_node(self):
        self.next.append({})
        self.end.append(False)
        self.size += 1
        return self.size - 1

    def insert(self, word):
        cur_node = self.root
        for char in word:
            idx = ord(char)
            if idx not in self.next[cur_node].keys():
                self.next[cur_node][idx] = self.create_new_node()
            cur_node = self.next[cur_node][idx]
        self.end[cur_node] = True

    def match(self, word):
        cur_len = 0
        max_match_len = 0
        cur_node = self.root
        for char in word:
            idx = ord(char)
            if idx not in self.next[cur_node].keys():
                break
            cur_node = self.next[cur_node][idx]
            cur_len += 1
            if self.end[cur_node]:
                max_match_len = cur_len
        return max_match_len
