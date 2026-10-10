
class Node:
    def __init__(self, criterion, document, status="PENDING"):
        self.criterion = criterion
        self.document = document
        self.status = status
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        node.prev = self.tail
        node.next = None

        if self.tail:
            self.tail.next = node
        else:
            self.head = node

        self.tail = node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None

    def nodes(self):
        current = self.head
        while current:
            yield current
            current = current.next


class YearData:
    def __init__(self):
        self.documents = {}
        self.order = LinkedList()
        self.undo = []

    def get(self, criterion, document):
        return self.documents.get(criterion, {}).get(document)

    def add(self, criterion, document, status="PENDING"):
        if self.get(criterion, document) is not None:
            raise ValueError("Document already exists")

        node = Node(criterion, document, status)
        self.documents.setdefault(criterion, {})[document] = node
        self.order.append(node)
        return node

    def remove(self, node):
        self.order.remove(node)
        del self.documents[node.criterion][node.document]

        if not self.documents[node.criterion]:
            del self.documents[node.criterion]

    def clear(self):
        self.documents.clear()
        self.order = LinkedList()


class EvidenceRepository:
    def __init__(self):
        self.years = {}

    def year(self, year):
        year = str(year)
        if year not in self.years:
            self.years[year] = YearData()
        return self.years[year]

    def add(self, year, criterion, document):
        data = self.year(year)
        data.add(criterion, document)
        data.undo.append(("ADD", criterion, document))
        return "OK ADD"

    def submit(self, year, criterion, document):
        data = self.year(year)
        node = data.get(criterion, document)

        if node is None:
            raise ValueError("Document not found")

        if node.status == "SUBMITTED":
            raise ValueError("Already submitted")

        data.undo.append(("STATUS", criterion, document, node.status))
        node.status = "SUBMITTED"
        return "OK SUBMIT"

    def copyfwd(self, source, destination):
        source = str(source)
        destination = str(destination)

        if source == destination:
            raise ValueError("Years must differ")

        src = self.year(source)
        dst = self.year(destination)

        # Save the destination's complete previous state.
        snapshot = [
            (n.criterion, n.document, n.status)
            for n in dst.order.nodes()
        ]
        dst.undo.append(("RESTORE", snapshot))

        # Replace the destination structure.
        dst.clear()

        # All copied documents must start as PENDING.
        for node in src.order.nodes():
            dst.add(node.criterion, node.document, "PENDING")

        return "OK COPYFWD"

    def pending(self, year):
        data = self.year(year)
        docs = [
            f"{n.criterion}/{n.document}"
            for n in data.order.nodes()
            if n.status == "PENDING"
        ]
        return f"PENDING {year}: " + ",".join(docs)

    def rollback(self, year):
        data = self.year(year)

        if not data.undo:
            return f"NOTHING TO UNDO {year}"

        record = data.undo.pop()
        operation = record[0]

        if operation == "ADD":
            node = data.get(record[1], record[2])
            if node is not None:
                data.remove(node)

        elif operation == "STATUS":
            node = data.get(record[1], record[2])
            if node is not None:
                node.status = record[3]

        elif operation == "RESTORE":
            data.clear()
            for criterion, document, status in record[1]:
                data.add(criterion, document, status)

        return f"OK ROLLBACK {year}"

    def diff(self, year1, year2):
        a = self.year(year1)
        b = self.year(year2)

        keys_a = {
            (n.criterion, n.document) for n in a.order.nodes()
        }
        keys_b = {
            (n.criterion, n.document) for n in b.order.nodes()
        }

        def fmt(items):
            return ",".join(
                f"{c}/{d}" for c, d in sorted(items)
            ) or "-"

        return (
            f"DIFF {year1} {year2}\n"
            f"ONLY {year1}: {fmt(keys_a - keys_b)}\n"
            f"ONLY {year2}: {fmt(keys_b - keys_a)}"
        )

    def search(self, document):
        matches = []

        for year, data in self.years.items():
            for node in data.order.nodes():
                if document.lower() in node.document.lower():
                    matches.append(
                        f"{year}: {node.criterion}/"
                        f"{node.document} [{node.status}]"
                    )

        return "\n".join(matches) if matches else "NO MATCHES"


def execute(repo, command):
    parts = command.split()
    if not parts:
        return ""

    op = parts[0].upper()

    if op == "ADD" and len(parts) == 4:
        return repo.add(*parts[1:])

    elif op == "SUBMIT" and len(parts) == 4:
        return repo.submit(*parts[1:])

    elif op == "COPYFWD" and len(parts) == 3:
        return repo.copyfwd(*parts[1:])

    elif op == "PENDING" and len(parts) == 2:
        return repo.pending(parts[1])

    elif op == "ROLLBACK" and len(parts) == 2:
        return repo.rollback(parts[1])

    elif op == "DIFF" and len(parts) == 3:
        return repo.diff(parts[1], parts[2])

    elif op == "SEARCH" and len(parts) == 2:
        return repo.search(parts[1])

    else:
        raise ValueError("Invalid command or arguments")


def main():
    repo = EvidenceRepository()

    print("Academic-Year Evidence Repository")
    print("Commands: ADD, SUBMIT, COPYFWD, PENDING,")
    print("          ROLLBACK, DIFF, SEARCH, EXIT")

    while True:
        try:
            command = input("> ").strip()

            if command.upper() == "EXIT":
                break

            result = execute(repo, command)
            print(result)

        except ValueError as error:
            print(f"ERROR: {error}")


if __name__ == "__main__":
    main()