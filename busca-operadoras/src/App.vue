<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Busca de Operadoras</h1>

    <input
      v-model="termo"
      @input="buscarOperadoras"
      type="text"
      placeholder="Digite o nome da operadora"
      class="p-2 border rounded w-full mb-4"
    />

    <div v-if="operadoras.length === 0" class="text-gray-500">
      Nenhuma operadora encontrada.
    </div>

    <ul>
      <li
        v-for="operadora in operadoras"
        :key="operadora.cd_operadora"
        class="mb-2"
      >
        <div class="p-4 bg-white shadow rounded">
          <strong>{{ operadora.nome_operadora }}</strong
          ><br />
          Código: {{ operadora.cd_operadora }}
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      termo: "",
      operadoras: [],
    };
  },
  methods: {
    async buscarOperadoras() {
      if (this.termo.trim() === "") {
        this.operadoras = [];
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/buscar_operadoras`,
          {
            params: { termo: this.termo },
          }
        );
        this.operadoras = response.data;
      } catch (error) {
        console.error("Erro ao buscar operadoras:", error);
      }
    },
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f3f4f6;
}
</style>
