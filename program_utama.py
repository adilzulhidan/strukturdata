import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

FILE_CSV = 'datamahasiswa.csv'

class MahasiswaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplikasi Nilai Mahasiswa")

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        
        ttk.Button(self.frame, text="Tambah Data Mahasiswa", command=self.tambah_data).grid(row=0, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Lihat Semua Data", command=self.lihat_data).grid(row=1, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Cari Mahasiswa", command=self.cari_data).grid(row=2, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Hitung Rata-Rata Nilai", command=self.rata_rata_nilai).grid(row=3, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Nilai Tertinggi/Terendah", command=self.nilai_extreme).grid(row=4, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Hapus Data Mahasiswa", command=self.hapus_data).grid(row=5, column=0, sticky="ew", pady=2)
        ttk.Button(self.frame, text="Keluar", command=master.quit).grid(row=6, column=0, sticky="ew", pady=2)


        self.text = tk.Text(master, height=15, width=60)
        self.text.pack(padx=10, pady=10)

    def tambah_data(self):
        nim = simpledialog.askstring("Input", "Masukkan NIM:")
        if not nim: return
        nama = simpledialog.askstring("Input", "Masukkan Nama:")
        if not nama: return
        matkul = simpledialog.askstring("Input", "Masukkan Mata Kuliah:")
        if not matkul: return
        nilai = simpledialog.askstring("Input", "Masukkan Nilai:")
        if not nilai: return

        try:
            with open(FILE_CSV, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nim, nama, matkul, nilai])
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def lihat_data(self):
        self.text.delete(1.0, tk.END)
        try:
            with open(FILE_CSV, mode='r') as file:
                reader = csv.reader(file)
                self.text.insert(tk.END, "=== Data Mahasiswa ===\n")
                for row in reader:
                    self.text.insert(tk.END, f"NIM: {row[0]}, Nama: {row[1]}, Mata Kuliah: {row[2]}, Nilai: {row[3]}\n")
        except FileNotFoundError:
            self.text.insert(tk.END, "⚠️  File belum ada. Silakan tambahkan data terlebih dahulu.\n")

    def cari_data(self):
        keyword = simpledialog.askstring("Cari", "Masukkan NIM atau Nama untuk dicari:")
        if not keyword: return
        keyword = keyword.lower()
        ditemukan = False
        self.text.delete(1.0, tk.END)
        try:
            with open(FILE_CSV, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if keyword in row[0].lower() or keyword in row[1].lower():
                        self.text.insert(tk.END, f"✅ Ditemukan: NIM: {row[0]}, Nama: {row[1]}, Mata Kuliah: {row[2]}, Nilai: {row[3]}\n")
                        ditemukan = True
                if not ditemukan:
                    self.text.insert(tk.END, "❌ Data tidak ditemukan.\n")
        except FileNotFoundError:
            self.text.insert(tk.END, "⚠️  File belum ada.\n")

    def rata_rata_nilai(self):
        total = 0
        count = 0
        self.text.delete(1.0, tk.END)
        try:
            with open(FILE_CSV, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        total += float(row[3])
                        count += 1
                    except ValueError:
                        continue
            if count > 0:
                self.text.insert(tk.END, f"📊 Rata-rata nilai mahasiswa adalah: {total / count:.2f}\n")
            else:
                self.text.insert(tk.END, "⚠️  Tidak ada data nilai yang bisa dihitung.\n")
        except FileNotFoundError:
            self.text.insert(tk.END, "⚠️  File belum ada.\n")

    def hapus_data(self):
        nim_target = simpledialog.askstring("Hapus Data", "Masukkan NIM Mahasiswa yang ingin dihapus:")
        if not nim_target:
            return
        try:
            with open(FILE_CSV, mode='r') as file:
                reader = list(csv.reader(file))
                data_baru = [row for row in reader if row[0] != nim_target]

            if len(data_baru) == len(reader):
                messagebox.showinfo("Info", "Data dengan NIM tersebut tidak ditemukan.")
            else:
                with open(FILE_CSV, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data_baru)
                messagebox.showinfo("Sukses", f"Data dengan NIM {nim_target} berhasil dihapus.")
                self.lihat_data()
        except FileNotFoundError:
            messagebox.showwarning("File Tidak Ditemukan", "File data belum tersedia.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def nilai_extreme(self):
        nilai_tertinggi = None
        nilai_terendah = None
        data_tertinggi = []
        data_terendah = []
        self.text.delete(1.0, tk.END)
        try:
            with open(FILE_CSV, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        nilai = float(row[3])
                        if (nilai_tertinggi is None) or (nilai > nilai_tertinggi):
                            nilai_tertinggi = nilai
                            data_tertinggi = [row]
                        elif nilai == nilai_tertinggi:
                            data_tertinggi.append(row)

                        if (nilai_terendah is None) or (nilai < nilai_terendah):
                            nilai_terendah = nilai
                            data_terendah = [row]
                        elif nilai == nilai_terendah:
                            data_terendah.append(row)
                    except ValueError:
                        continue

            self.text.insert(tk.END, "🏆 Mahasiswa dengan Nilai Tertinggi:\n")
            for dt in data_tertinggi:
                self.text.insert(tk.END, f"{dt[1]} ({dt[0]}) - Nilai: {dt[3]}\n")

            self.text.insert(tk.END, "\n📉 Mahasiswa dengan Nilai Terendah:\n")
            for dt in data_terendah:
                self.text.insert(tk.END, f"{dt[1]} ({dt[0]}) - Nilai: {dt[3]}\n")
        except FileNotFoundError:
            self.text.insert(tk.END, "⚠️  File belum ada.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MahasiswaApp(root)
    root.mainloop()
