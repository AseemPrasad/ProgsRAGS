<script lang="ts">
  import './app.css'
  
  let query = '';
  let loading = false;
  let result: any = null;

  async function handleSearch() {
    if (!query) return;
    loading = true;
    try {
      // Mocking the API call for MVP demo
      // In production: const res = await fetch(`http://localhost:8000/query?q=${encodeURIComponent(query)}`);
      // result = await res.json();
      
      // Delay for effect
      await new Promise(r => setTimeout(r, 1000));
      
      result = {
        answer: "Based on the **Q3 Financial Report**, revenue increased by 15% [Source: Q3_2024_Report.pdf, Page 4]. However, according to the **Internal Memo**, there were concerns about margin compression in the EMEA region [Source: EMEA_Memo_2024.pdf, Page 1].",
        confidence: "medium",
        sources: [
          { title: "Q3_2024_Report.pdf", page: 4, content: "Revenue growth was driven by cloud sales..." },
          { title: "EMEA_Memo_2024.pdf", page: 1, content: "Margin compression remains a key risk..." }
        ],
        conflicts: [
          { type: "temporal", description: "Source A (2024) conflicts with Source B (2022) policy." }
        ]
      };
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h1 style="text-align: center; margin-bottom: 40px;">Knowledge Intelligence</h1>
  
  <div class="card">
    <form on:submit|preventDefault={handleSearch}>
      <input 
        type="text" 
        bind:value={query} 
        placeholder="Search enterprise knowledge..." 
        disabled={loading}
      />
    </form>
  </div>

  {#if loading}
    <div style="text-align: center; color: var(--text-secondary);">Analyzing sources...</div>
  {/if}

  {#if result}
    {#if result.conflicts && result.conflicts.length > 0}
      <div class="conflict-banner">
        <span>⚠️</span>
        <div>
          <strong>Potential Conflicts Detected</strong>
          <p style="margin: 0; font-size: 13px;">{result.conflicts[0].description}</p>
        </div>
      </div>
    {/if}

    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
        <h3 style="margin: 0;">Verified Answer</h3>
        <span class="badge badge-{result.confidence}">Confidence: {result.confidence}</span>
      </div>
      
      <p style="line-height: 1.6;">{result.answer}</p>

      <div style="margin-top: 24px;">
        <h4 style="margin-bottom: 12px; font-size: 14px; text-transform: uppercase; color: var(--text-secondary);">Sources & Evidence</h4>
        {#each result.sources as source}
          <div class="source-item">
            <strong>{source.title}</strong> — Page {source.page}
            <p style="margin: 4px 0 0 0; font-style: italic; font-size: 13px;">"{source.content}"</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</main>

<style>
  main {
    width: 100%;
  }
</style>
