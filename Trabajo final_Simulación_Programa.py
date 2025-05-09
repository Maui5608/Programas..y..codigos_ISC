
import math
import matplotlib.pyplot as plt

def factorial(n):
    return math.factorial(n)

def calc_p0(lmbda, mu, s, K):
    rho = lmbda / (s * mu)
    sum_terms = sum([(lmbda / mu) ** n / factorial(n) for n in range(s)])
    last_term = ((lmbda / mu) ** s / factorial(s)) * ((1 - rho ** (K - s + 1)) / (1 - rho)) if rho != 1 else (K - s + 1)
    return 1 / (sum_terms + last_term)

def calc_pk(lmbda, mu, s, K, P0):
    rho = lmbda / (s * mu)
    return ((lmbda / mu) ** K / (factorial(s) * s ** (K - s))) * P0

def mm_s_k(lmbda, mu, s, K):
    rho = lmbda / (s * mu)
    P0 = calc_p0(lmbda, mu, s, K)
    PK = calc_pk(lmbda, mu, s, K, P0)
    L = sum([
        n * ((lmbda / mu) ** n / factorial(n)) * P0 if n < s else
        n * ((lmbda / mu) ** s / factorial(s)) * ((lmbda / (s * mu)) ** (n - s)) * P0
        for n in range(1, K + 1)
    ])
    Lq = L - (lmbda * (1 - PK) / mu)
    W = L / (lmbda * (1 - PK))
    Wq = Lq / (lmbda * (1 - PK))

    results = {
        "λ (tasa de llegada)": lmbda,
        "μ (tasa de servicio)": mu,
        "s (número de servidores)": s,
        "K (capacidad del sistema)": K,
        "ρ (utilización)": round(rho, 4),
        "P0 (probabilidad sistema vacío)": round(P0, 4),
        "PK (probabilidad de pérdida)": round(PK, 4),
        "L (clientes promedio en el sistema)": round(L, 2),
        "Lq (clientes promedio en la cola)": round(Lq, 2),
        "W (tiempo promedio en el sistema)": round(W, 2),
        "Wq (tiempo promedio en la cola)": round(Wq, 2),
    }

    return results

def main():
    print("Modelo M/M/s/K para cafetería")
    lmbda = float(input("Ingrese la tasa de llegada λ (clientes por hora): "))
    mu = float(input("Ingrese la tasa de servicio μ (clientes atendidos por mesero por hora): "))
    s = int(input("Ingrese el número de meseros (servidores): "))
    K = int(input("Ingrese la capacidad máxima del sistema (número de mesas): "))

    results = mm_s_k(lmbda, mu, s, K)

    for key, value in results.items():
        print(f"{key}: {value}")

    labels = ["L", "Lq", "W", "Wq"]
    values = [results["L (clientes promedio en el sistema)"],
              results["Lq (clientes promedio en la cola)"],
              results["W (tiempo promedio en el sistema)"],
              results["Wq (tiempo promedio en la cola)"]]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['skyblue', 'orange', 'green', 'red'])
    plt.title("Indicadores del sistema M/M/s/K")
    plt.ylabel("Valor")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
