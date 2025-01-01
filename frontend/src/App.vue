<script setup>
import { ref } from 'vue'

const image = ref(null)
const imageUrl = ref(null)
const loading = ref(false)
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
    const result = await response.json();
    switch (result.type) {
      case 1:
        alert('犬🐕です');
        break;
      case 2:
        alert('猫🐈です');
        break;
      case 3:
        alert('犬🐕と猫🐈のどちらでもないです');
        break;
      default:
        alert('判定できませんでした');
        break;
    }
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
      <div v-if="image" class="image-preview">
        <img :src="imageUrl" alt="Uploaded Image" />
      </div>
      <form @submit.prevent="postImage" method="post" enctype="multipart/form-data" class="form">
        <label class="file-input">
          <input v-on:change="handleFileChange" type="file" name="file" accept="image/*" required />
          <span>画像を選択</span>
        </label>
        <button type="submit" class="upload-button">判定する</button>
      </form>
    </div>
  </main>
</template>

<style scoped>
/* 全体の背景 */
body {
  background: linear-gradient(-45deg, #6e8efb, #a777e3, #f0f4ff, #d8e4ff);
  background-size: 400% 400%;
  animation: gradient-animation 15s ease infinite;  font-family: 'Roboto', sans-serif;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #fff;
}
@keyframes gradient-animation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}


/* コンテナ */
.container {
  display: flex;
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
</style>
