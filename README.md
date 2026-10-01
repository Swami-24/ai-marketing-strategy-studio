# AI Marketing Strategy Studio

A Streamlit web app based on the uploaded notebook's problem statement: a startup has developed a lightweight water bottle, the target audience is school children aged 6–16, and the example marketing budget is USD 2,000.

## Workflow
1. **Agent 1 — Marketing Strategist:** creates campaign objectives, channel recommendations, budget allocation, a four-week timeline, and KPIs.
2. **Agent 2 — Content Creator:** uses Agent 1's strategy to create social posts, a short-video script, headlines, and a parent/guardian-facing message.
3. **Export:** the user can download a Markdown campaign report.

The deployed web app uses two sequential Gemini API calls to implement the notebook's two-agent workflow. It is a Streamlit app, not a direct deployment of the original AutoGen notebook.

## Files to upload to GitHub
- `app.py`
- `requirements.txt`
- `README.md` (optional but recommended)
- `.streamlit/config.toml` (optional UI theme)

**Do not upload your API key or a `secrets.toml` containing the key.**

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository, for example `ai-marketing-strategy-studio`.
2. Upload `app.py`, `requirements.txt`, and `README.md` to the repository root.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
5. In the deployed app's settings, open **Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your-real-Gemini-API-key"
   ```

6. Save the secrets and wait for the app to build. Open the generated app URL and test the Generate campaign button.

Get a key at https://aistudio.google.com/apikey. Keep it private and never commit it to GitHub.

## Run locally
Use Python 3.11 or 3.12. In a terminal in this folder:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` locally with:

```toml
GEMINI_API_KEY = "your-real-Gemini-API-key"
```

Then run:

```bash
streamlit run app.py
```

Do not upload the local `secrets.toml` file to GitHub.
