# Contributing

## Development principles
- Keep the project runnable after each milestone.
- Add tests with every behavior change.
- Preserve deterministic builds and stable ranking tie-breaks.
- Benchmark before optimizing and publish methodology with results.
- Do not commit corpus dumps, index artifacts, model weights, secrets, or benchmark output containing sensitive data.

## Pull request checklist
- [ ] Tests added or updated
- [ ] Formatting, linting, and type checks pass
- [ ] API/schema compatibility considered
- [ ] Quality impact measured when ranking changes
- [ ] Performance impact measured when hot paths change
- [ ] Documentation and architecture decisions updated
- [ ] Security and failure behavior considered
