class SistemaGestionTickets:
    def __init__(self):
        self.tickets = []
        self.contador_id = 1

    def registrar_ticket(self, ticket):
        self.tickets.append(ticket)

    def generar_id(self):
        id_generado = self.contador_id
        self.contador_id += 1
        return id_generado

    def buscar_por_id(self, id_ticket):
        for ticket in self.tickets:
            if ticket.id == id_ticket:
                return ticket
        return None

    def filtrar_por_estado(self, estado):
        return [t for t in self.tickets if t.estado == estado]

    def filtrar_por_tipo(self, tipo):
        if tipo == "todos":
            return self.tickets
        return [t for t in self.tickets if t.tipo == tipo]

    def contar_por_tipo(self):
        conteo = {"todos": len(self.tickets), "red": 0, "hardware": 0, "software": 0, "cuenta": 0}
        for ticket in self.tickets:
            conteo[ticket.tipo] = conteo.get(ticket.tipo, 0) + 1
        return conteo
