"""
Struktur Data Aplikasi Note-Taking
====================================
Latihan: Rancang struktur data untuk aplikasi note-taking yang mendukung:
  1. Multiple tags per note        -> TagIndex  (multi-linked by tag)
  2. Chronological & alphabetical  -> DoublyLinkedList (doubly linked sorted)
  3. Sync status tracking          -> CircularBuffer  (circular buffer)
"""

from datetime import datetime


# ══════════════════════════════════════════════════════
# 1. NoteNode — satu catatan sekaligus simpul DLL
# ══════════════════════════════════════════════════════
class NoteNode:
    def __init__(self, note_id: int, title: str, content: str):
        self.note_id    = note_id
        self.title      = title
        self.content    = content
        self.created_at = datetime.now()
        self.tags       = []

        # Pointer Doubly Linked List kronologis
        self.prev_chrono = None
        self.next_chrono = None

        # Pointer Doubly Linked List alfabetis
        self.prev_alpha  = None
        self.next_alpha  = None

    def __repr__(self):
        return f"Note(id={self.note_id}, title={self.title!r}, tags={self.tags})"


# ══════════════════════════════════════════════════════
# 2. TagIndex — indeks multi-linked by tag
# ══════════════════════════════════════════════════════
class TagIndex:
    def __init__(self):
        self._index = {}    # { tag_str: [NoteNode, ...] }

    def add(self, tag: str, note: NoteNode):
        self._index.setdefault(tag, [])
        if note not in self._index[tag]:
            self._index[tag].append(note)
        if tag not in note.tags:
            note.tags.append(tag)

    def remove(self, tag: str, note: NoteNode):
        if tag in self._index:
            self._index[tag] = [n for n in self._index[tag] if n is not note]
            if not self._index[tag]:
                del self._index[tag]
        if tag in note.tags:
            note.tags.remove(tag)

    def get_notes_by_tag(self, tag: str):
        return self._index.get(tag, [])


# ══════════════════════════════════════════════════════
# 3. DoublyLinkedList — sorted (chrono ATAU alpha)
# ══════════════════════════════════════════════════════
class DoublyLinkedList:
    """
    mode='chrono' : urut berdasarkan created_at
    mode='alpha'  : urut berdasarkan title a→z
    Satu NoteNode bisa sekaligus berada di kedua DLL
    karena masing-masing punya set pointer berbeda.
    """
    def __init__(self, mode: str = "chrono"):
        self.mode  = mode
        self.head  = None
        self.tail  = None
        self._size = 0

    def _prev(self, n): return n.prev_chrono if self.mode=="chrono" else n.prev_alpha
    def _next(self, n): return n.next_chrono if self.mode=="chrono" else n.next_alpha
    def _set_prev(self, n, v):
        if self.mode=="chrono": n.prev_chrono = v
        else:                   n.prev_alpha  = v
    def _set_next(self, n, v):
        if self.mode=="chrono": n.next_chrono = v
        else:                   n.next_alpha  = v
    def _key(self, n):
        return n.created_at if self.mode=="chrono" else n.title.lower()

    def insert(self, note: NoteNode):
        if self.head is None:
            self.head = self.tail = note
            self._set_prev(note, None); self._set_next(note, None)
        else:
            cur = self.head
            while cur and self._key(cur) <= self._key(note):
                cur = self._next(cur)
            if cur is None:
                self._set_prev(note, self.tail); self._set_next(note, None)
                self._set_next(self.tail, note); self.tail = note
            elif self._prev(cur) is None:
                self._set_prev(note, None); self._set_next(note, cur)
                self._set_prev(cur, note); self.head = note
            else:
                p = self._prev(cur)
                self._set_prev(note, p); self._set_next(note, cur)
                self._set_next(p, note); self._set_prev(cur, note)
        self._size += 1

    def remove(self, note: NoteNode):
        p, nx = self._prev(note), self._next(note)
        if p:  self._set_next(p, nx)
        else:  self.head = nx
        if nx: self._set_prev(nx, p)
        else:  self.tail = p
        self._set_prev(note, None); self._set_next(note, None)
        self._size -= 1

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur); cur = self._next(cur)
        return result


# ══════════════════════════════════════════════════════
# 4. CircularBuffer — sync status tracking
# ══════════════════════════════════════════════════════
class SyncChange:
    def __init__(self, note_id: int, action: str):
        self.note_id   = note_id
        self.action    = action     # 'CREATE' | 'UPDATE' | 'DELETE'
        self.timestamp = datetime.now()
        self.synced    = False

    def __repr__(self):
        status = "synced " if self.synced else "pending"
        return f"[{status}] {self.action:6s} note#{self.note_id} @ {self.timestamp:%H:%M:%S}"


class CircularBuffer:
    """
    Array kapasitas tetap; ketika penuh, entri terlama
    otomatis tertimpa (FIFO overwrite).
    """
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._buf     = [None] * capacity
        self._head    = 0   # posisi tulis berikutnya
        self._count   = 0

    def push(self, change: SyncChange):
        self._buf[self._head] = change
        self._head  = (self._head + 1) % self.capacity
        self._count = min(self._count + 1, self.capacity)

    def get_recent(self):
        result = []
        for i in range(self._count):
            idx = (self._head - 1 - i) % self.capacity
            if self._buf[idx]: result.append(self._buf[idx])
        return result

    def mark_synced(self, note_id: int):
        for x in self._buf:
            if x and x.note_id == note_id: x.synced = True

    def pending_changes(self):
        return [c for c in self.get_recent() if not c.synced]


# ══════════════════════════════════════════════════════
# 5. NoteManager — orkestrasi semua struktur data
# ══════════════════════════════════════════════════════
class NoteManager:
    def __init__(self, sync_buffer_size: int = 10):
        self._notes   = {}
        self._next_id = 1
        self.tag_index   = TagIndex()
        self.chrono_list = DoublyLinkedList(mode="chrono")
        self.alpha_list  = DoublyLinkedList(mode="alpha")
        self.sync_buffer = CircularBuffer(capacity=sync_buffer_size)

    def create_note(self, title, content, tags=None) -> NoteNode:
        note = NoteNode(self._next_id, title, content)
        self._next_id += 1
        self._notes[note.note_id] = note
        self.chrono_list.insert(note)
        self.alpha_list.insert(note)
        for tag in (tags or []): self.tag_index.add(tag, note)
        self.sync_buffer.push(SyncChange(note.note_id, "CREATE"))
        return note

    def update_note(self, note_id, title=None, content=None):
        note = self._notes.get(note_id)
        if not note: return None
        if title and title != note.title:
            self.alpha_list.remove(note)
            note.title = title
            self.alpha_list.insert(note)
        if content: note.content = content
        self.sync_buffer.push(SyncChange(note_id, "UPDATE"))
        return note

    def delete_note(self, note_id) -> bool:
        note = self._notes.pop(note_id, None)
        if not note: return False
        self.chrono_list.remove(note)
        self.alpha_list.remove(note)
        for tag in list(note.tags): self.tag_index.remove(tag, note)
        self.sync_buffer.push(SyncChange(note_id, "DELETE"))
        return True

    def view_chronological(self):  return self.chrono_list.to_list()
    def view_alphabetical(self):   return self.alpha_list.to_list()
    def view_by_tag(self, tag):    return self.tag_index.get_notes_by_tag(tag)
    def view_recent_changes(self): return self.sync_buffer.get_recent()
    def view_pending_sync(self):   return self.sync_buffer.pending_changes()


# ══════════════════════════════════════════════════════
# DEMO
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    nm = NoteManager(sync_buffer_size=8)

    n1 = nm.create_note("Belajar Python",  "OOP dan struktur data", ["python","belajar"])
    n2 = nm.create_note("Algoritma Sort",  "Bubble, merge, quick",  ["python","algoritma"])
    n3 = nm.create_note("Database Design", "ERD dan normalisasi",   ["database","belajar"])
    n4 = nm.create_note("API REST",        "RESTful endpoint",      ["backend","python"])
    n5 = nm.create_note("Zaman Keemasan",  "Sejarah ilmu",          ["sejarah"])

    print("=== Kronologis ===")
    for n in nm.view_chronological():
        print(f"  {n.note_id}. {n.title} | tags:{n.tags}")

    print("\n=== Alfabetis ===")
    for n in nm.view_alphabetical():
        print(f"  {n.note_id}. {n.title}")

    print("\n=== Tag 'python' ===")
    for n in nm.view_by_tag("python"):
        print(f"  - {n.title}")

    nm.update_note(n1.note_id, title="Advanced Python")
    nm.delete_note(n3.note_id)

    print("\n=== Alfabetis (setelah update & delete) ===")
    for n in nm.view_alphabetical():
        print(f"  {n.note_id}. {n.title} | tags:{n.tags}")

    print("\n=== Recent Changes ===")
    for c in nm.view_recent_changes(): print(f"  {c}")

    nm.sync_buffer.mark_synced(n1.note_id)
    nm.sync_buffer.mark_synced(n2.note_id)

    print("\n=== Pending Sync ===")
    pending = nm.view_pending_sync()
    for c in pending: print(f"  {c}")
    if not pending: print("  Semua sudah di-sync!")