# Academic-Year Evidence Repository

A Python-based, command-line document management system designed to organize academic evidence across multiple academic years. It supports document status tracking, copy-forward operations, rollback, year-wise comparison, and cross-year search using fundamental data structures and algorithms.

Developed as part of the **Contest-Based Learning Hackathon – Coding Challenge** organized by the Department of Computer Science and Engineering, **SRM Institute of Science and Technology (SRMIST), Tiruchirappalli**.

## Features

- **Academic-Year Management** — Organize evidence by academic year, criterion, and document name.
- **Document Status Tracking** — Add documents with a default `PENDING` status and mark them as `SUBMITTED`.
- **Copy Forward** — Copy a year's document structure to another year; copied documents start with `PENDING` status.
- **Rollback / Undo** — Reverse the most recent supported operation for a specific academic year.
- **Year-wise Difference (DIFF)** — Compare two years and identify documents present in only one of them.
- **Cross-Year Search** — Find document names across stored academic years using a case-insensitive partial match.
- **Ordered Document Management** — Maintain document order with a doubly linked list.
- **Hierarchical Lookup** — Store documents in nested dictionaries grouped by criterion and document name.

## Tech Stack and Concepts

- **Language:** Python 3
- **Data Structures:** Nested dictionaries, doubly linked lists, stacks
- **Algorithms / Concepts:** Set operations, searching, rollback, state snapshots, time and space complexity

## Getting Started

### Prerequisites

- Python 3.8 or later recommended
- No third-party packages are required by the current implementation

### Run the project

1. Clone the repository:

   ```bash
   git clone https://github.com/Asmi0102/YOUR-REPOSITORY.git
   ```

2. Move into the project directory:

   ```bash
   cd YOUR-REPOSITORY
   ```

3. Run the Python file (replace `main.py` with your actual filename if different):

   ```bash
   python main.py
   ```

## Available Commands

Commands use space-separated arguments. In the current implementation, criterion and document names must not contain spaces.

| Command | Syntax | Description |
|---|---|---|
| Add a document | `ADD <year> <criterion> <document>` | Adds a document with `PENDING` status. |
| Submit a document | `SUBMIT <year> <criterion> <document>` | Marks an existing document as `SUBMITTED`. |
| Copy forward | `COPYFWD <source_year> <destination_year>` | Replaces the destination year's document structure with a copy of the source; copied statuses reset to `PENDING`. |
| List pending documents | `PENDING <year>` | Displays documents still marked `PENDING` for a year. |
| Roll back | `ROLLBACK <year>` | Undoes the latest recorded operation for that year, if available. |
| Compare years | `DIFF <year1> <year2>` | Shows documents unique to each of the two years. |
| Search documents | `SEARCH <document>` | Searches document names across years using a case-insensitive partial match. |
| Exit | `EXIT` | Closes the program. |

## Example Session

```text
Academic-Year Evidence Repository
Commands: ADD, SUBMIT, COPYFWD, PENDING,
          ROLLBACK, DIFF, SEARCH, EXIT
> ADD 2025-26 NAAC AnnualReport
OK ADD
> ADD 2025-26 NBA CourseFiles
OK ADD
> SUBMIT 2025-26 NAAC AnnualReport
OK SUBMIT
> PENDING 2025-26
PENDING 2025-26: NBA/CourseFiles
> COPYFWD 2025-26 2026-27
OK COPYFWD
> PENDING 2026-27
PENDING 2026-27: NAAC/AnnualReport,NBA/CourseFiles
> SEARCH Annual
2025-26: NAAC/AnnualReport [SUBMITTED]
2026-27: NAAC/AnnualReport [PENDING]
> DIFF 2025-26 2026-27
DIFF 2025-26 2026-27
ONLY 2025-26: -
ONLY 2026-27: -
> ROLLBACK 2026-27
OK ROLLBACK 2026-27
> EXIT
```

*Note: The exact ordering of search results follows the order in which academic years and documents were stored.*

## How It Works

### Data organization

- `EvidenceRepository` manages the collection of academic years.
- `YearData` stores a year's documents, their order, and its undo history.
- `Node` represents an individual document and stores its criterion, name, status, and linked-list pointers.
- `LinkedList` maintains document insertion order and supports node removal.
- The nested dictionary enables direct lookup by criterion and document name.
- Sets are used by `DIFF` to identify documents unique to either year.
- Each year's `undo` list acts as a stack of operation records.

### Rollback behavior

The repository records undo information for `ADD`, `SUBMIT`, and `COPYFWD`. A rollback affects only the selected year. For copy-forward, the previous destination state is saved so it can be restored.

## Complexity Notes

Let **n** be the number of documents in a year and **m** the total number of documents across all years.

| Operation | Expected / Typical Complexity |
|---|---|
| Look up a document | Expected `O(1)` dictionary lookup |
| Add a document | Expected `O(1)` lookup and linked-list append |
| Submit a document | Expected `O(1)` lookup and status update |
| Remove a known node | `O(1)` linked-list update, plus dictionary operations |
| List pending documents | `O(n)` |
| Copy forward | `O(n + d)`, where `d` is the previous destination size |
| Compare two years | Expected `O(n + k)` where `k` is the size of the second year, excluding output sorting |
| Search across years | `O(m)` string checks, excluding the cost of each substring comparison |

These are typical complexity estimates; actual costs depend on string lengths, hash-table behavior, and output formatting.

## Current Limitations

- This is an in-memory command-line application. Data is not saved after the program exits.
- Commands split arguments on spaces, so criterion and document names cannot currently contain spaces.
- `COPYFWD` replaces the destination year's existing document structure.
- Rollback history is maintained in memory and is not persisted.
- The implementation has no graphical user interface or multi-user access control.

## Future Improvements

- Add persistent storage using SQLite or another database.
- Support quoted arguments and document names containing spaces.
- Add automated unit tests for normal and edge cases.
- Improve transactional safety and validation for copy-forward operations.
- Add import/export functionality and a graphical or web interface.

## Learning Outcomes

This project demonstrates practical application of data structures and algorithms to a document-management problem, including hierarchical data organization, linked-list operations, stack-based undo, set-based comparison, and complexity analysis.

## Author

**Asmi0102**

- GitHub: [@Asmi0102](https://github.com/Asmi0102)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
