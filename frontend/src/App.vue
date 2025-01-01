<script setup>
import { ref,reactive } from 'vue'

const image = ref(null)
const imageUrl = ref(null)
const loading = ref(false)
const result = reactive({
  type: 0,
  dog: 0.0,
  cat: 0.0,
})
const api = import.meta.env.VITE_API_URL

function handleFileChange(event) {
  image.value = event.target.files[0];
  if(image.value) {
    /**
     * URL.createObjectURL()は、指定されたBlobオブジェクトやFileオブジェクトを参照する新しいオブジェクトURLを生成します。
     * revokeObjectURL()は、以前に生成されたオブジェクトURLを解放しメモリリークを防ぎます。
     */
    URL.revokeObjectURL(imageUrl.value);
    imageUrl.value = URL.createObjectURL(image.value);
  }
}
async function postImage() {
  loading.value = true;
  try {
    const response = await fetch(api, {
      method: 'POST',
      body: image.value
    });
    const json = await response.json();
    result.type = json.type;
    result.dog = json.dog;
    result.cat = json.cat;
  } catch (error) {
    console.error(error);
    alert('Failed to upload image');
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main class="container">
    <div class="card">
      <h1>Dog or Cat</h1>
      <p>AIがアップロードされた画像を猫🐈か犬🐕か判定します</p>
      <div v-show="image" class="image-preview">
        <img :src="imageUrl" alt="Uploaded Image" />
      </div>
      <form @submit.prevent="postImage" method="post" enctype="multipart/form-data" class="form">
        <label class="file-input">
          <input v-on:change="handleFileChange" type="file" name="file" accept="image/*" required />
          <span>画像を選択</span>
        </label>
        <button :disabled="loading" type="submit" class="upload-button">{{loading?"判定中...":"判定する"}}</button>
      </form>
    </div>
    <div v-show="!loading && result.cat" class="card result">
      <h2>判定結果</h2>
      <p>{{ result.type ? "犬🐕":"猫🐈"}}</p>
      <p>猫確率:{{ Math.trunc(result.cat * 100) }} % <br>
         犬確率:{{ Math.trunc(result.dog * 100) }} %</p>
    </div>
  </main>
</template>

<style scoped>
/* コンテナ */
.container {
  display: flex;
  flex-direction: column; /* 縦方向に配置 */
  justify-content: center;
  align-items: center;
  height: 100%;
}

/* カードデザイン */
.card {
  background: #ffffff;
  color: #333;
  border-radius: 12px;
  padding: 30px;
  margin-top: 30px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* 見出し */
.card h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

/* 説明テキスト */
.card p {
  font-size: 16px;
  margin-bottom: 20px;
  color: #666;
}

/* 画像プレビュー */
.image-preview {
  margin-bottom: 20px;
}

.image-preview img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* フォーム */
.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* ファイル入力 */
.file-input {
  display: inline-block;
  position: relative;
  overflow: hidden;
  color: #6e8efb;
  font-weight: bold;
  cursor: pointer;
}

.file-input input {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-input span {
  display: block;
  background: #f0f4ff;
  padding: 10px 20px;
  border-radius: 5px;
  text-align: center;
  transition: background 0.3s ease;
}

.file-input:hover span {
  background: #d8e4ff;
}

/* アップロードボタン */
.upload-button {
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
}

.upload-button:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
.result{
  transition: transform 0.3s ease; /* アニメーションの時間を0.3秒に設定 */
}
.result:hover{
  transform: scale(1.2); /* 回転と拡大 */
}
  </style>
