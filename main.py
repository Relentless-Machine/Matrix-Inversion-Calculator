import tkinter as tk
from tkinter import simpledialog, scrolledtext, IntVar, Label
import sympy as sp

class MatrixInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Inversion Calculator")

        self.rows = 0
        self.columns = 0
        self.matrix_entries = []
        self.display_type_var = IntVar()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Matrix Inversion Calculator", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), sticky="ew")

        intro_label = tk.Label(self.root, text="Input Matrix:", justify="center")
        intro_label.grid(row=1, column=0, columnspan=3, pady=(10, 5), sticky="ew")

        self.get_matrix_size()
        self.create_matrix_entries()
        self.create_display_options()

        button_width = 15

        submit_button = tk.Button(self.root, text="Submit", command=self.on_submit, width=button_width)
        submit_button.grid(row=self.rows + 5, column=0, columnspan=self.columns + 3, pady=5)

        update_button = tk.Button(self.root, text="Update Size", command=self.update_matrix_size, width=button_width)
        update_button.grid(row=self.rows + 6, column=0, columnspan=self.columns + 3, pady=5)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, width=button_width, fg="red")
        exit_button.grid(row=self.rows + 7, column=0, columnspan=self.columns + 3, pady=5)

        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10)
        self.result_text.grid(row=self.rows + 8, column=0, columnspan=self.columns + 3, pady=10)

        self.error_label = Label(self.root, text="", fg="red")
        self.error_label.grid(row=self.rows + 9, column=0, columnspan=self.columns + 3, pady=5)

        self.display_type_var.trace_add("write", self.update_result)

    def get_matrix_size(self):
        try:
            self.rows = simpledialog.askinteger("Input", "Enter the number of rows:")
            self.columns = simpledialog.askinteger("Input", "Enter the number of columns:")
        except ValueError:
            self.display_error("Please enter valid numeric values for rows and columns.")

    def create_matrix_entries(self):
        self.matrix_entries = [[None for _ in range(self.columns)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                entry = tk.Entry(self.root, width=15)
                entry.grid(row=i + 3, column=j, padx=5, pady=5, sticky="nsew")
                self.matrix_entries[i][j] = entry

        for i in range(self.rows):
            self.root.grid_rowconfigure(i + 3, weight=1)

        for j in range(self.columns):
            self.root.grid_columnconfigure(j, weight=1)

    def create_display_options(self):
        display_options_label = tk.Label(self.root, text="Display Type:")
        display_options_label.grid(row=self.rows + 3, column=0, columnspan=self.columns + 3, pady=(10, 5))

        fraction_button = tk.Radiobutton(self.root, text="Fraction", variable=self.display_type_var, value=0)
        fraction_button.grid(row=self.rows + 4, column=self.columns // 2 - 1, pady=(0, 5), sticky="e")

        decimal_button = tk.Radiobutton(self.root, text="Decimal", variable=self.display_type_var, value=1)
        decimal_button.grid(row=self.rows + 4, column=self.columns // 2, pady=(0, 5), sticky="w")

        self.display_type_var.set(0)

    def on_submit(self):
        self.error_label.config(text="")
        self.update_result()

    def update_result(self, *args):
        matrix = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                value = self.matrix_entries[i][j].get()
                try:
                    row.append(sp.Rational(value))
                except ValueError:
                    self.display_error("Please enter valid numeric values in all cells.")
                    return
            matrix.append(row)

        try:
            sympy_matrix = sp.Matrix(matrix)
            inverse_matrix = sympy_matrix.inv()

            sp.init_printing(use_unicode=True, wrap_line=False)

            display_type = self.display_type_var.get()

            if display_type == 0:
                inverse_elements_formatted = [
                    [
                        sp.nsimplify(element) if isinstance(element, sp.Rational) else element
                        for element in row
                    ]
                    for row in inverse_matrix.tolist()
                ]
            else:
                inverse_elements_formatted = [
                    [
                        float(element) if isinstance(element, sp.Rational) else element
                        for element in row
                    ]
                    for row in inverse_matrix.tolist()
                ]

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Inverse Matrix:\n")

            for row in inverse_elements_formatted:
                row_str = [f"{element}" for element in row]
                self.result_text.insert(tk.END, f"[{', '.join(map(str, row_str))}]\n")

        except sp.matrices.common.MatrixError:
            self.display_error("Matrix is not invertible.")

    def display_error(self, message):
        self.error_label.config(text=message, fg="red", font=("Helvetica", 12, "bold"))

    def update_matrix_size(self):
        self.root.destroy()
        new_window = tk.Tk()
        app = MatrixInputApp(new_window)

def main():
    root = tk.Tk()
    app = MatrixInputApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
