import express from "express";
import { promisify } from 'util';
import { createClient } from 'redis';

const client = createClient();

const app = express()

const port = 1245;

const listProducts = [
    {itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4},
    {itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10},
    {itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2},
    {itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5},
]

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const getItemById = (id) => {
    return listProducts.find((item) => item.itemId === id)
}

app.get('/list_products', (req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json')
    res.json(listProducts)
})

const reserveStockById = (itemId, stock) => {
    client.SET(`item.${itemId}`, stock);
}

const getCurrentReservedStockById = async (itemId) => {
    const clientGet = promisify(client.GET).bind(client);
    return await clientGet(`item.${itemId}`);
}


app.get('/list_products/:itemId', (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(+itemId);
    if (product) {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json')
        getCurrentReservedStockById(itemId).then((reservedStock) => {
            reservedStock = +reservedStock || 0;
            console.log(reservedStock)
            product.currentQuantity = product.initialAvailableQuantity - reservedStock
            res.json(product)
        })
    } else {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'application/json')
        res.json({"status":"Product not found"})
    }
})

app.get('/reserve_product/:itemId', (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(+itemId);
    if (!product) {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'application/json');
        res.json({"status": "Product not found" });
    } else {
        getCurrentReservedStockById(itemId).then((reservedStock) => {
            reservedStock = +reservedStock || 0;
            // product.currentQuantity = product.initialAvailableQuantity - reservedStock
            if (reservedStock >= product.initialAvailableQuantity) {
                res.json({"status":"Not enough stock available","itemId":itemId})
            } else {
                console.log(reservedStock)
                reserveStockById(itemId, reservedStock + 1).
                res.json({"status":"Reservation confirmed","itemId":itemId})
            }
        })
    }
})

app.listen(port, () => {
    console.log(`Server listening on PORT ${port}`);
});

