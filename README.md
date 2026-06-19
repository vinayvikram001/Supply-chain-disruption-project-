# Supply-chain-disruption-project-
Logistics &amp; Supply Chain - Autonomous Disruption Monitoring Agent,Global supply chains are highly fragile. Port strikes, extreme weather, or geopolitical conflicts can disrupt production, making it crucial to quickly identify alternative suppliers across all supply chain tiers.

## Running the API

From the project root, start the API with:

```bash
python main.py
```

The API will be available at:
- http://localhost:8000/health
- http://localhost:8000/docs

## API endpoints

- `GET /health` - checks whether the model artifacts are available
- `POST /predict` - predicts recovery time from disruption data
