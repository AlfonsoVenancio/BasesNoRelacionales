/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package generatecases;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.Random;
import java.time.LocalDate;
import java.time.Month;
import javax.json.Json;
import javax.json.JsonObjectBuilder;
/**
 *
 * @author alfon
 */
public class GenerateCases {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String[] empresas = {"PEMEX","BANAMEX","BIMBO","CEMEX","GRUMA"};
        String[] tiposDeAcciones = {"ord","pre","pri"};
        LocalDate fecha = LocalDate.of(2014, Month.SEPTEMBER, 1);
        try{
            FileWriter escritorAcciones = new FileWriter("acciones.jsonl");
            
            //BufferedWriter escritorAcciones = new BufferedWriter(archivoAcciones);
            
            FileWriter escritorDividendos = new FileWriter("dividendos.jsonl");
            //BufferedWriter escritorDividendos = new BufferedWriter(archivoDividendos);
            
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
            
            while(fecha.isBefore(LocalDate.of(2019, Month.OCTOBER, 1))){         
                for(Accion accionHoy : acciones){
                    accionHoy.CambiaPrecioAccion();
                    escritorAcciones.write(accionHoy.toJSON().add("Fecha", fecha.toString()).build().toString() + "\n");
                }
                if(fecha.plusDays(1).getDayOfMonth() == 1){
                    // Reparto de dividendos y compra/venta de acciones
                    // Al final del mes
                    for(Accion accionHoy : acciones){
                        Double pagoDividendo = accionHoy.CostoAccion * accionHoy.PorcentajeDividendos;
                        String pago = Json.createObjectBuilder()
                                .add("Id", accionHoy.Id)
                                .add("Pago", pagoDividendo)
                                .add("Fecha", fecha.toString()).build().toString();
                        escritorDividendos.write(pago + "\n");
                    }
                }
                fecha = fecha.plusDays(1);
            }
            escritorAcciones.close();
            escritorDividendos.close();
        }catch(IOException e){
            System.err.format("IOEcception: %s%n",e);
        }
    }
    
}

class Accion{
    public static Integer IdAccion = 0;
    public String Id;
    public String Empresa;
    public String TipoAccion;
    public Double CostoAccion;
    public Double PorcentajeDividendos;
    
    public Accion(String Empresa, String TipoAccion, Double CostoAccion, Double PorcentajeDividendos){
        this.Id = Empresa.substring(0, 4) + String.valueOf(++IdAccion);
        this.Empresa = Empresa;
        this.TipoAccion = TipoAccion;
        this.CostoAccion = CostoAccion;
        this.PorcentajeDividendos = PorcentajeDividendos;
    }
    
    public void CambiaPrecioAccion(){
        Random manoInvisible = new Random();
        this.CostoAccion += this.CostoAccion * ((manoInvisible.nextDouble() - 0.5) * 0.1);
    }
    
    public JsonObjectBuilder toJSON(){
        return Json.createObjectBuilder()
                .add("Id", Id).add("Empresa", Empresa)
                .add("TipoAccion", TipoAccion)
                .add("CostoAccion", CostoAccion)
                .add("PorcentajeDividendos", PorcentajeDividendos);
    }
}
