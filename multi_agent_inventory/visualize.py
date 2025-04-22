import matplotlib.pyplot as plt

def plot_inventory_data(products_data):
    """
    products_data: dict where key=product_id, value=dict with 'days', 'stock', 'demand'
    Example:
    {
        1001: {'days': [1, 2, 3], 'stock': [100, 90, 80], 'demand': [20, 15, 10]},
        1002: {'days': [1, 2, 3], 'stock': [200, 190, 170], 'demand': [25, 30, 20]},
    }
    """
    num_products = len(products_data)
    cols = 2  # Adjust this based on your layout preference
    rows = (num_products + 1) // cols

    fig, axs = plt.subplots(rows, cols, figsize=(12, 5 * rows))
    axs = axs.flatten()  # Make it easier to loop over

    for idx, (product_id, data) in enumerate(products_data.items()):
        ax = axs[idx]
        ax.plot(data['days'], data['stock'], label='Stock', marker='o')
        ax.plot(data['days'], data['demand'], label='Demand', marker='x')
        ax.set_title(f"Product ID: {product_id}")
        ax.set_xlabel("Day")
        ax.set_ylabel("Units")
        ax.legend()
        ax.grid(True)

    # Hide any unused subplots
    for i in range(idx + 1, len(axs)):
        fig.delaxes(axs[i])

    plt.tight_layout()
    plt.show()