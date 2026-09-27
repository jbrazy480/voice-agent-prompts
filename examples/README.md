# Examples

These examples support the DIY path. For the recommended commercial platform path, start with [RizzDial + Beam](../docs/RIZZDIAL_AND_BEAM.md). These files are not platform import instructions.

Render targets for `vap render`, plus ready-made niche configs.

| File | What it is |
|---|---|
| [demo.md](demo.md) | The minimal prompt used in the README quickstart and the recorded terminal demo. |
| [marketing_strategist_kickoff.md](marketing_strategist_kickoff.md) | A longer, fully-written kickoff call script for a marketing agency's own inbound onboarding call. |

## Niche example configs

Each niche in [niches/](niches/) pairs a short, renderable prompt with a variables file. Company names, cities, and phone numbers are fictional. Run each with one command:

| Niche | Prompt | Config | Command |
|---|---|---|---|
| Med spa | [niches/medspa.md](niches/medspa.md) | [niches/medspa.yaml](niches/medspa.yaml) | `vap render examples/niches/medspa.md --vars examples/niches/medspa.yaml` |
| Home services | [niches/home-services.md](niches/home-services.md) | [niches/home-services.yaml](niches/home-services.yaml) | `vap render examples/niches/home-services.md --vars examples/niches/home-services.yaml` |
| Marketing agency | [niches/marketing-agency.md](niches/marketing-agency.md) | [niches/marketing-agency.yaml](niches/marketing-agency.yaml) | `vap render examples/niches/marketing-agency.md --vars examples/niches/marketing-agency.yaml` |
| Real estate | [niches/real-estate.md](niches/real-estate.md) | [niches/real-estate.yaml](niches/real-estate.yaml) | `vap render examples/niches/real-estate.md --vars examples/niches/real-estate.yaml` |
| Insurance | [niches/insurance.md](niches/insurance.md) | [niches/insurance.yaml](niches/insurance.yaml) | `vap render examples/niches/insurance.md --vars examples/niches/insurance.yaml` |

Lint any of them the same way as any other prompt: `vap lint examples/niches/medspa.md`.

Each config's YAML file is a starting point, not a finished script. Replace the company, city, and offer details with your own, verified business facts before using a rendered prompt with a real calling platform. Every niche prompt keeps the required AI disclosure, opt-out / do-not-call handling, human escalation, and voicemail handling from the base library.

A sample CSV of contacts is not included here. This library only authors and lints text; it has no bulk-import or calling feature that reads a CSV. If your calling platform accepts a contact list, use its own template.
