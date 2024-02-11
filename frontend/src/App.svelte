<script>
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/vite.svg";
  import Counter from "./lib/Counter.svelte";

  let files;
  let qn;

  $: if (files) {
    // Note that `files` is of type `FileList`, not an Array:
    // https://developer.mozilla.org/en-US/docs/Web/API/FileList
    console.log(files);

    for (const file of files) {
      console.log(`${file.name}: ${file.size} bytes`);
    }
  }

  async function askQn() {
    // ${files.map(file => file.name)}
    const formData = new FormData();
    formData.append("db_id", "123");
    formData.append("question_text", qn);

    const response = await fetch("http://localhost:8080/askqn", {
      method: "POST",
      body: formData,
    }).then((x) => x.json());
    return response;
  }

  let promise;
  function handleAskQnClick() {
    promise = askQn().then((x) => JSON.stringify(x));
  }

  async function uploadFiles() {
    const formData = new FormData();
    formData.append("db_id", "123");
    // TODO: support more than one file
    formData.append("uploaded_file", files[0]);
    try {
      const response = await fetch("http://localhost:8080/upload", {
        mode: "no-cors", // no-cors, *cors, same-origin
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      console.log("Success:", result);
      return result;
    } catch (error) {
      console.error("Error:", error);
      return error;
    }
  }
  function handleUploadFilesClick() {
    promise = uploadFiles().then((x) => JSON.stringify(x));
  }
</script>

<main>
  <div>
    <label for="many">Upload multiple files of any type:</label>
    <input bind:files id="many" multiple type="file" />

    {#if files}
      <h2>Selected files:</h2>
      {#each Array.from(files) as file}
        <p>{file.name} ({file.size} bytes)</p>
      {/each}
    {/if}

    <button
      style="margin-left: -3em;"
      on:click={handleUploadFilesClick}
      disabled={!files}>upload</button
    >
  </div>

  <div style="padding-top: 1em;">
    <textarea bind:value={qn} />
    <button on:click={handleAskQnClick} disabled={!qn}>askqn</button>
  </div>

  <output class="text-output">
    {#await promise}
      <p>...waiting</p>
    {:then result}
      <p>{result}</p>
    {:catch error}
      <p style="color: red">{error.message}</p>
    {/await}
  </output>
</main>

<style>
  .text-output {
    font-size: larger;
  }
</style>
