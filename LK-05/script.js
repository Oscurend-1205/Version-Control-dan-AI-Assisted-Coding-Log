const form = document.getElementById("formPendaftaran");
const hasil = document.getElementById("hasilPendaftaran");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const nama = document.getElementById("nama").value;
  const email = document.getElementById("email").value;
  const nohp = document.getElementById("hp").value;
  const kategori = document.getElementById("kategori").value;
  const pesan = document.getElementById("pesan").value;

  if (nama === "" || email === "" || nohp === "" || kategori === "") {
    alert("Semua field wajib diisi");
    return;
  }

  if (!email.includes("@")) {
    alert("Email tidak valid!");
    return;
  }

  hasil.innerHTML = `
<div style="margin-top:20px; padding:15px; background:#f1f5f9; border-radius:10px;">
    <h3>Data Berhasil Dikirim!</h3>
    <p><strong>Nama:</strong> ${nama}</p>
    <p><strong>Email:</strong> ${email}</p>
    <p><strong>No HP:</strong> ${nohp}</p>
    <p><strong>Kategori:</strong> ${kategori}</p>
    <p><strong>Pesan:</strong> ${pesan}</p>
    </div>
`;

  alert("Pesan berhasil dikirim!");

  form.reset();
});

document.getElementById("nama").addEventListener("input", function () {
  console.log("User sedang mengetik nama...");
});
