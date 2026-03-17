## Workflow Orchestration

1. **Plan Mode Default**
    - Use `superpower:brainstorm` skill (if available) or plan mode for ANY non-trivial task (3+ steps or architectural decisions)
    - If something goes sideways, STOP and re-plan immediately – don't keep pushing
    - Use plan mode for verification steps, not just building
    - Write detailed specs upfront to reduce ambiguity
2. **Subagent Strategy**
    - Use subagents liberally to keep main context window clean
    - Offload research, exploration, and parallel analysis to subagents
    - For complex problems, throw more compute at it via subagents
    - One track per subagent for focused execution
3. **Self-Improvement Loop**
    - After ANY correction from the user, write rules for yourself that prevent the same mistake
    - **Capture Lessons**: Update `.lessons.md` after corrections
    - **Never** git commit `.lessons.md`.
    - Ruthlessly iterate on these lessons until mistake rate drops
    - Review lessons at session start for relevant project
4. **Verification Before Done**
    - Never mark a task complete without proving it works
    - Diff behavior between main and your changes when relevant
    - Ask yourself: "Would a staff engineer approve this?"
    - Run tests, check logs, demonstrate correctness
5. **Demand Elegance (Balanced)**
    - For non-trivial changes: pause and ask "is there a more elegant way?"
    - If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
    - Skip this for simple, obvious fixes – don't over-engineer
    - Challenge your own work before presenting it
6. **Autonomous Bug Fixing**
    - When given a bug report: just fix it. Don't ask for hand-holding
    - Point at logs, errors, failing tests – then resolve them
    - Zero context switching required from the user
    - Go fix failing CI tests without being told how

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior staff developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Write Clean Code**: Follow clean code guideline and write easy to understand code.

## Clean Code Guideline

### Constants Over Magic Numbers

- Replace hard-coded values with named constants.
- Use descriptive constant names that explain the value's purpose.
- Keep constants at the top of the file or in a dedicated constants file.

### Meaningful Names

- Variables, functions, and classes should reveal their purpose.
- Names should explain why something exists and how it's used.
- Avoid abbreviations unless they're universally understood.

### Smart Comments

- Don't comment on what the code does - make the code self-documenting.
- Use comments to explain why something is done a certain way.
- Document APIs, complex algorithms, and non-obvious side effects.
- Always end comment with a period.

### Single Responsibility

- Each function should do exactly one thing.
- Functions should be small and focused.
- If a function needs a comment to explain what it does, it should be split.

### DRY (Don't Repeat Yourself)

- Extract repeated code into reusable functions.
- Share common logic through proper abstraction.
- Maintain single sources of truth.

### Clean Structure

- Keep related code together.
- Organize code in a logical hierarchy.
- Use consistent file and folder naming conventions.

### Encapsulation

- Hide implementation details.
- Expose clear interfaces.
- Move nested conditionals into well-named functions.

### Code Quality Maintenance

- Refactor continuously.
- Fix technical debt early.
- Leave code cleaner than you found it.

### Testing

- Write tests before fixing bugs.
- Keep tests readable and maintainable.
- Test edge cases and error conditions.