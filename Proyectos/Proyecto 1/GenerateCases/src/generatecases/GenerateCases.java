import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.Random;
import java.time.LocalDate;
import java.time.Month;
import javax.json.Json;
import javax.json.JsonObjectBuilder;

public class GenerateCases {
    public static void main(String[] args) {
        // Fecha inicial para generar los datos
        LocalDate fecha = LocalDate.of(2014, Month.SEPTEMBER, 1);
        try{
            // Los dos objetos para escribir a los archivos
            FileWriter escritorAcciones = new FileWriter("acciones.jsonl");
            FileWriter escritorDividendos = new FileWriter("dividendos.jsonl");
            
            // Arreglo de acciones de las que queremos generar datos
            Accion[] acciones = {
                new Accion("PEMEX","ord",15000.0,0.15),
                new Accion("BANAMEX","ord",23000.0,0.13),
                new Accion("CEMEX","pre",60000.0,0.13),
                new Accion("BIMBO","ord",9000.0,0.08),
                new Accion("PEMEX","pri",45000.0,0.15),
                new Accion("BIMBO","ord",80000.0,0.15),
                new Accion("BANAMEX","ord",24000.0,0.19),
                new Accion("CEMEX","pre",45000.0,0.12),
                new Accion("BANAMEX","pri",27000.0,0.14),
                new Accion("PEMEX","pre",20000.0,0.10),
                new Accion("BIMBO","ord",50000.0,0.15),
                new Accion("CEMEX","pre",23000.0,0.11)
            };
            
            // Se generan los datos hasta el primero de octubre de 2019
            while(fecha.isBefore(LocalDate.of(2019, Month.OCTOBER, 1))){
                // Para cada una de las acciones, se hace una modificacion de su precio y se escribe el JSON al archivo correspondiente     
                for(Accion accionHoy : acciones){
                    accionHoy.CambiaPrecioAccion();
                    escritorAcciones.write(accionHoy.toJSON().add("Fecha", fecha.toString()).build().toString() + "\n");
                }
                if(fecha.plusDays(1).getDayOfMonth() == 1){
                    // Reparto de dividendos y compra/venta de acciones
                    // Al final del mes
                    for(Accion accionHoy : acciones){
                        // Se obtienen el pago de dividendos de esta accion y se escribe el JSON al archivo
                        Double pagoDividendo = accionHoy.CostoAccion * accionHoy.PorcentajeDividendos;
                        String pago = Json.createObjectBuilder()
                                .add("Id", accionHoy.Id)
                                .add("Pago", pagoDividendo)
                                .add("Fecha", fecha.toString()).build().toString();
                        escritorDividendos.write(pago + "\n");
                    }
                }
                // Siguiente dia
                fecha = fecha.plusDays(1);
            }
            escritorAcciones.close();
            escritorDividendos.close();
        }catch(IOException e){
            System.err.format("IOException: %s%n",e);
        }
    }
    
}

// lol
class Accion{
    public static Integer IdAccion = 0;
    public String Id;
    public String Empresa;
    public String TipoAccion;
    public Double CostoAccion;
    public Double PorcentajeDividendos;
    
    public Accion(String Empresa, String TipoAccion, Double CostoAccion, Double PorcentajeDividendos){
        // El Id de la accion son los primeros 4 caracteres del nombre de la ccion y un numero entero consecutivo entre todas las acciones
        this.Id = Empresa.substring(0, 4) + String.valueOf(++IdAccion);
        this.Empresa = Empresa;
        this.TipoAccion = TipoAccion;
        this.CostoAccion = CostoAccion;
        this.PorcentajeDividendos = PorcentajeDividendos;
    }
    
    // Cada que se le quiere cambiar el precio a una accion, se le suma o resta aleatoriamente el 5% de su costo de ese dia
    public void CambiaPrecioAccion(){
        Random manoInvisible = new Random();
        this.CostoAccion += this.CostoAccion * ((manoInvisible.nextDouble() - 0.5) * 0.1);
    }
    
    // Se agregan todos los miembros al JSON y se devuelve un JSONObjectBuilder para poder agregarle mas datos
    public JsonObjectBuilder toJSON(){
        return Json.createObjectBuilder()
                .add("Id", Id).add("Empresa", Empresa)
                .add("TipoAccion", TipoAccion)
                .add("CostoAccion", CostoAccion)
                .add("PorcentajeDividendos", PorcentajeDividendos);
    }
}
